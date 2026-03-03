#!/usr/bin/env python3
"""
Download datasheets for components found in a KiCad project directory.

Default behavior:
- Assumes this script is placed in the KiCad project root directory.
- Scans all `.kicad_sch` files in that directory recursively.
- Extracts component metadata (Datasheet URL, MPN, Manufacturer, LCSC code, etc.).
- Downloads datasheets into `./datasheets`.
- If a datasheet source appears non-English, attempts to find an English fallback.
- Prints status directly to stdout.
"""

from __future__ import annotations

import dataclasses
import hashlib
import html
import os
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0 Safari/537.36"
)

REQUEST_TIMEOUT_SECONDS = 25
MAX_HTML_BYTES = 1_500_000
MAX_SEARCH_RESULTS_TO_TRY = 8
MAX_PDF_INSPECTION_BYTES = 2_500_000
MAX_COMPONENT_RESOLUTION_SECONDS = 12
MOUSER_API_BASE_URL = "https://api.mouser.com/api/v1.0"
ENABLE_WEB_SEARCH_DEFAULT = os.getenv("DATASHEET_ENABLE_WEB_SEARCH", "").strip().lower() in {
    "1",
    "true",
    "yes",
    "on",
}
MOUSER_API_KEY_DEFAULT = (
    os.getenv("DATASHEET_MOUSER_API_KEY", "").strip()
    or os.getenv("MOUSER_API_KEY", "").strip()
)

PLACEHOLDER_VALUES = {"", "~", "n/a", "na", "-", "none", "null"}

NON_ENGLISH_HINTS = (
    "/cn/",
    ".cn/",
    "zh-cn",
    "zh_cn",
    "zh-tw",
    "zh_tw",
    "lang=cn",
    "lang=zh",
    "locale=cn",
    "locale=zh",
)

BAD_PDF_TEXT_HINTS = (
    "datasheet unavailable",
    "document unavailable",
    "file unavailable",
    "temporarily unavailable",
    "no datasheet",
    "not found",
    "404",
    "forbidden",
    "access denied",
    "internal use only",
    "do not distribute",
    "draft only",
    "sample only",
    "confidential",
    "under non-disclosure",
    "暂无",
    "不可用",
    "保密",
)

GOOD_PDF_TEXT_HINTS = (
    "datasheet",
    "absolute maximum ratings",
    "recommended operating conditions",
    "electrical characteristics",
    "functional block diagram",
    "pin configuration",
    "ordering information",
    "application information",
    "typical characteristics",
)

IDENTIFIER_SPLIT_RE = re.compile(r"[\s,;/|()\\]+")
NON_ALNUM_RE = re.compile(r"[^A-Za-z0-9]+")


@dataclasses.dataclass
class Component:
    source_file: str
    source_kind: str
    symbol_name: str
    reference: str
    value: str
    datasheet: str
    manufacturer: str
    manufacturer_part: str
    lcsc: str
    description: str

    def unique_key(self) -> Tuple[str, ...]:
        return (
            normalize_token(self.datasheet),
            normalize_token(self.manufacturer_part),
            normalize_token(self.lcsc),
            normalize_token(self.manufacturer),
            normalize_token(self.value),
            normalize_token(self.symbol_name),
        )

    def label(self) -> str:
        return (
            self.manufacturer_part
            or self.lcsc
            or self.reference
            or self.value
            or self.symbol_name
            or "component"
        )

    def query_terms(self) -> List[str]:
        terms: List[str] = []
        if self.manufacturer_part:
            terms.append(self.manufacturer_part)
        if self.manufacturer:
            terms.append(self.manufacturer)
        if self.lcsc:
            terms.append(self.lcsc)
        if self.value:
            terms.append(self.value)
        if self.symbol_name:
            terms.append(self.symbol_name)
        return terms


def normalize_token(value: str) -> str:
    return value.strip().lower()


def is_placeholder(value: str) -> bool:
    return normalize_token(value) in PLACEHOLDER_VALUES


def clean_value(value: str) -> str:
    value = html.unescape(value.strip())
    return value.replace('\\"', '"').replace("\\\\", "\\")


def safe_slug(value: str, max_len: int = 80) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip())
    slug = slug.strip("._-")
    if not slug:
        slug = "component"
    return slug[:max_len]


def find_kicad_files(project_root: Path) -> List[Path]:
    return sorted(set(project_root.rglob("*.kicad_sch")))


def find_matching_paren(text: str, start_index: int) -> int:
    depth = 0
    in_string = False
    escaped = False
    for i in range(start_index, len(text)):
        ch = text[i]
        if escaped:
            escaped = False
            continue
        if ch == "\\" and in_string:
            escaped = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i
    return -1


def read_head_token(text: str, open_paren_index: int) -> str:
    i = open_paren_index + 1
    while i < len(text) and text[i].isspace():
        i += 1
    start = i
    while i < len(text) and (not text[i].isspace()) and text[i] not in ('(', ')', '"'):
        i += 1
    return text[start:i]


def extract_blocks(text: str, head_token: str) -> List[str]:
    blocks: List[str] = []
    i = 0
    in_string = False
    escaped = False
    while i < len(text):
        ch = text[i]
        if escaped:
            escaped = False
            i += 1
            continue
        if ch == "\\" and in_string:
            escaped = True
            i += 1
            continue
        if ch == '"':
            in_string = not in_string
            i += 1
            continue
        if in_string:
            i += 1
            continue
        if ch == "(":
            token = read_head_token(text, i)
            if token == head_token:
                end = find_matching_paren(text, i)
                if end != -1:
                    blocks.append(text[i : end + 1])
                    i = end + 1
                    continue
        i += 1
    return blocks


PROPERTY_RE = re.compile(r'\(\s*property\s+"([^"]+)"\s+"((?:\\.|[^"\\])*)"', re.MULTILINE)
SYMBOL_NAME_RE = re.compile(r'^\(\s*symbol\s+"([^"]+)"')
LIB_ID_RE = re.compile(r'\(\s*lib_id\s+"([^"]+)"')


def parse_component_from_symbol_block(block: str, source_file: str, source_kind: str) -> Component:
    props: Dict[str, str] = {}
    for prop_name, prop_value in PROPERTY_RE.findall(block):
        key = clean_value(prop_name)
        val = clean_value(prop_value)
        # Keep first non-empty value for a property key.
        if key not in props or (is_placeholder(props[key]) and not is_placeholder(val)):
            props[key] = val

    symbol_name = ""
    match = SYMBOL_NAME_RE.search(block)
    if match:
        symbol_name = clean_value(match.group(1))
    if not symbol_name:
        lib_match = LIB_ID_RE.search(block)
        if lib_match:
            symbol_name = clean_value(lib_match.group(1))

    def first(*keys: str) -> str:
        for key in keys:
            value = props.get(key, "").strip()
            if value and not is_placeholder(value):
                return value
        return ""

    return Component(
        source_file=source_file,
        source_kind=source_kind,
        symbol_name=symbol_name,
        reference=first("Reference"),
        value=first("Value"),
        datasheet=first("Datasheet"),
        manufacturer=first("Manufacturer"),
        manufacturer_part=first("Manufacturer Part", "MPN", "Part Number"),
        lcsc=first("LCSC", "LCSC Part", "LCSC Part #"),
        description=first("Description", "ki_description"),
    )


def extract_components_from_file(path: Path) -> List[Component]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    blocks = extract_blocks(text, "symbol")
    source_kind = "schematic" if path.suffix == ".kicad_sch" else "symbol_library"
    components = [
        parse_component_from_symbol_block(
            block=block,
            source_file=str(path),
            source_kind=source_kind,
        )
        for block in blocks
    ]
    return components


def normalize_url(url: str) -> str:
    url = clean_value(url)
    if not url:
        return ""
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme:
        return ""
    return url


def looks_like_url(value: str) -> bool:
    try:
        parsed = urllib.parse.urlparse(value)
        return parsed.scheme in {"http", "https"} and bool(parsed.netloc)
    except Exception:
        return False


def likely_non_english_url(url: str) -> bool:
    lurl = url.lower()
    if any(hint in lurl for hint in NON_ENGLISH_HINTS):
        return True
    if re.search(r"[^\x00-\x7F]", url):
        return True
    return False


def build_ti_english_url(component: Component) -> Optional[str]:
    manufacturer = component.manufacturer.lower()
    part = component.manufacturer_part.strip()
    if not part:
        return None
    if "texas instruments" in manufacturer or "ti" in manufacturer:
        cleaned = re.sub(r"[^a-zA-Z0-9.-]", "", part).lower()
        if cleaned:
            return f"https://www.ti.com/lit/gpn/{cleaned}"
    if part.upper().startswith(("TPS", "LM", "BQ", "TLV", "INA", "SN")):
        cleaned = re.sub(r"[^a-zA-Z0-9.-]", "", part).lower()
        if cleaned:
            return f"https://www.ti.com/lit/gpn/{cleaned}"
    return None


def decode_response_content(data: bytes, headers: Dict[str, str]) -> str:
    charset = "utf-8"
    content_type = headers.get("content-type", "")
    m = re.search(r"charset=([A-Za-z0-9._-]+)", content_type, re.IGNORECASE)
    if m:
        charset = m.group(1).strip()
    try:
        return data.decode(charset, errors="ignore")
    except LookupError:
        return data.decode("utf-8", errors="ignore")


def make_request(url: str, max_bytes: Optional[int] = None) -> Tuple[str, Dict[str, str], bytes]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as resp:
        final_url = resp.geturl()
        headers = {k.lower(): v for k, v in resp.headers.items()}
        if max_bytes is None:
            data = resp.read()
        else:
            data = resp.read(max_bytes)
        return final_url, headers, data


def make_json_post_request(url: str, payload: Dict[str, object]) -> Dict[str, object]:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "User-Agent": USER_AGENT,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as resp:
        data = resp.read(MAX_HTML_BYTES)
    decoded = data.decode("utf-8", errors="ignore")
    loaded = json.loads(decoded)
    if isinstance(loaded, dict):
        return loaded
    return {}


def normalize_part_id(value: str) -> str:
    return NON_ALNUM_RE.sub("", (value or "")).upper()


def first_dict_value_case_insensitive(d: Dict[str, object], keys: List[str]) -> str:
    lowered = {k.lower(): v for k, v in d.items()}
    for key in keys:
        value = lowered.get(key.lower())
        if isinstance(value, str):
            value = value.strip()
            if value:
                return value
    return ""


def mouser_search_parts(
    api_key: str,
    path: str,
    payload: Dict[str, object],
) -> List[Dict[str, object]]:
    try:
        response = make_json_post_request(f"{MOUSER_API_BASE_URL}{path}?apiKey={api_key}", payload)
    except Exception:
        return []
    if not isinstance(response, dict):
        return []

    errors = response.get("Errors")
    if isinstance(errors, list) and errors:
        return []

    search_results = response.get("SearchResults")
    if not isinstance(search_results, dict):
        return []
    parts = search_results.get("Parts")
    if not isinstance(parts, list):
        return []

    out: List[Dict[str, object]] = []
    for part in parts:
        if isinstance(part, dict):
            out.append(part)
    return out


def get_mouser_datasheet_candidates(
    component: Component,
    api_key: str,
    mouser_cache: Dict[str, List[str]],
) -> List[str]:
    part_number = component.manufacturer_part.strip()
    if not api_key or not part_number:
        return []

    cache_key = f"{normalize_part_id(part_number)}::{normalize_token(component.manufacturer)}"
    if cache_key in mouser_cache:
        return mouser_cache[cache_key]

    requests: List[Tuple[str, Dict[str, object]]] = []
    if component.manufacturer.strip():
        requests.append(
            (
                "/search/partnumberandmanufacturer",
                {
                    "SearchByPartMfrNameRequest": {
                        "mouserPartNumber": part_number,
                        "manufacturerName": component.manufacturer.strip(),
                        "partSearchOptions": "Exact",
                    }
                },
            )
        )
    requests.append(
        (
            "/search/partnumber",
            {
                "SearchByPartRequest": {
                    "mouserPartNumber": part_number,
                    "partSearchOptions": "Exact",
                }
            },
        )
    )

    exact_part = normalize_part_id(part_number)
    ranked: List[Tuple[int, str]] = []
    for path, payload in requests:
        for part in mouser_search_parts(api_key=api_key, path=path, payload=payload):
            datasheet_url = first_dict_value_case_insensitive(
                part,
                [
                    "DataSheetUrl",
                    "DataSheetURL",
                    "DatasheetUrl",
                    "DatasheetURL",
                ],
            )
            if not looks_like_url(datasheet_url):
                continue

            score = 0
            mouser_mpn = normalize_part_id(
                first_dict_value_case_insensitive(
                    part,
                    ["ManufacturerPartNumber", "ManufacturerPartNum", "PartNumber"],
                )
            )
            if mouser_mpn and mouser_mpn == exact_part:
                score += 100

            mouser_mfr = normalize_token(
                first_dict_value_case_insensitive(part, ["Manufacturer", "ManufacturerName"])
            )
            if component.manufacturer and mouser_mfr and component.manufacturer.lower() in mouser_mfr:
                score += 30

            score += 10
            ranked.append((score, datasheet_url))

    ranked.sort(key=lambda x: x[0], reverse=True)
    deduped: List[str] = []
    seen: Set[str] = set()
    for _score, url in ranked:
        if url in seen:
            continue
        seen.add(url)
        deduped.append(url)

    mouser_cache[cache_key] = deduped
    return deduped


HREF_RE = re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE)
RAW_PDF_URL_RE = re.compile(r'https?://[^\s"\'<>]+\.pdf(?:\?[^\s"\'<>]*)?', re.IGNORECASE)


def extract_links_from_html(html_text: str, base_url: str) -> List[str]:
    links: List[str] = []
    for href in HREF_RE.findall(html_text):
        href = html.unescape(href.strip())
        if not href:
            continue
        abs_url = urllib.parse.urljoin(base_url, href)
        if looks_like_url(abs_url):
            links.append(abs_url)
    for raw in RAW_PDF_URL_RE.findall(html_text):
        links.append(html.unescape(raw))

    deduped: List[str] = []
    seen: Set[str] = set()
    for link in links:
        if link not in seen:
            seen.add(link)
            deduped.append(link)
    return deduped


def score_pdf_candidate(url: str, prefer_english: bool) -> int:
    score = 0
    lurl = url.lower()
    if lurl.endswith(".pdf") or ".pdf?" in lurl:
        score += 10
    if "datasheet" in lurl:
        score += 5
    if "download" in lurl:
        score += 2
    if "search?" in lurl or "bing.com/search" in lurl or "google." in lurl:
        score -= 8
    if likely_non_english_url(url):
        score -= 6 if prefer_english else 1
    if prefer_english and any(x in lurl for x in ("/en/", "lang=en", "locale=en")):
        score += 4
    return score


def is_pdf_response(url: str, headers: Dict[str, str], data_prefix: bytes) -> bool:
    ctype = headers.get("content-type", "").lower()
    if "application/pdf" in ctype:
        return True
    lurl = url.lower()
    if lurl.endswith(".pdf") or ".pdf?" in lurl:
        return True
    return data_prefix.startswith(b"%PDF")


PRINTABLE_ASCII_RE = re.compile(rb"[ -~]{6,}")


def extract_pdf_text_signals(data: bytes) -> str:
    # Lightweight signal extraction without external dependencies.
    # This catches many "unavailable/confidential" placeholder PDFs.
    matches = PRINTABLE_ASCII_RE.findall(data[:MAX_PDF_INSPECTION_BYTES])
    if not matches:
        return ""
    text_parts: List[str] = []
    for chunk in matches[:9000]:
        try:
            text_parts.append(chunk.decode("latin1", errors="ignore"))
        except Exception:
            continue
    return " ".join(text_parts).lower()


def normalize_identifier(value: str) -> str:
    return NON_ALNUM_RE.sub("", value or "").upper()


def component_identifiers(component: Component) -> List[str]:
    identifiers: List[str] = []

    def add(value: str) -> None:
        norm = normalize_identifier(value)
        if len(norm) >= 5:
            identifiers.append(norm)

    if component.lcsc and re.fullmatch(r"C\d{3,}", component.lcsc.strip(), flags=re.IGNORECASE):
        add(component.lcsc)

    part = component.manufacturer_part.strip()
    if part:
        add(part)
        for piece in IDENTIFIER_SPLIT_RE.split(part):
            if piece:
                add(piece)

    deduped: List[str] = []
    seen: Set[str] = set()
    for ident in identifiers:
        if ident not in seen:
            seen.add(ident)
            deduped.append(ident)
    return deduped


def pdf_matches_component(url: str, pdf_text: str, component: Component) -> Tuple[bool, str]:
    identifiers = component_identifiers(component)
    if not identifiers:
        return True, "No strong component identifier; skipped strict identity match"

    haystack = normalize_identifier(urllib.parse.unquote(url)) + " " + normalize_identifier(pdf_text)
    matched = [ident for ident in identifiers if ident in haystack]
    if matched:
        return True, f"Matched identifiers: {', '.join(matched[:3])}"
    return False, "PDF content/URL does not match component identifiers"


def evaluate_pdf_quality(
    url: str,
    data: bytes,
    component: Optional[Component] = None,
) -> Tuple[bool, str]:
    if not data.startswith(b"%PDF"):
        return False, "Payload is not a valid PDF"
    if len(data) < 6_000:
        return False, "PDF payload is too small to be a real datasheet"

    text = extract_pdf_text_signals(data)
    if not text:
        # Could be image-only PDF; keep it.
        return True, "PDF accepted (no text signals available)"

    bad_hits = [hint for hint in BAD_PDF_TEXT_HINTS if hint in text]
    good_hits = [hint for hint in GOOD_PDF_TEXT_HINTS if hint in text]

    if bad_hits and not good_hits:
        return False, f"Rejected bad PDF text signals: {', '.join(bad_hits[:3])}"

    if "confidential" in text and len(good_hits) < 2:
        return False, "Rejected likely confidential/non-public document"

    lurl = url.lower()
    if "unavailable" in lurl or "notfound" in lurl:
        return False, "URL indicates unavailable/not-found document"

    if component is not None:
        ok, reason = pdf_matches_component(url, text, component)
        if not ok:
            return False, reason

    return True, "PDF quality checks passed"


def inspect_pdf_candidate(
    url: str,
    component: Component,
    inspection_cache: Dict[str, Tuple[bool, str]],
    strict_identity: bool = True,
) -> Tuple[bool, str]:
    cache_key = f"{url}::{component.unique_key()}::strict={1 if strict_identity else 0}"
    if cache_key in inspection_cache:
        return inspection_cache[cache_key]
    try:
        final_url, headers, data = make_request(url, max_bytes=MAX_PDF_INSPECTION_BYTES)
    except Exception as exc:
        result = (False, f"Inspection request failed: {exc}")
        inspection_cache[cache_key] = result
        return result

    if not is_pdf_response(final_url, headers, data[:8]):
        result = (False, "Candidate did not resolve to a PDF response")
        inspection_cache[cache_key] = result
        return result

    identity_component = component if strict_identity else None
    result = evaluate_pdf_quality(final_url, data, component=identity_component)
    inspection_cache[cache_key] = result
    return result


def parse_search_results_duckduckgo(html_text: str) -> List[str]:
    links = extract_links_from_html(html_text, "https://duckduckgo.com")
    out: List[str] = []
    for link in links:
        if "duckduckgo.com/l/" in link:
            parsed = urllib.parse.urlparse(link)
            qs = urllib.parse.parse_qs(parsed.query)
            uddg = qs.get("uddg", [""])[0]
            if uddg:
                link = urllib.parse.unquote(uddg)
        if looks_like_url(link):
            out.append(link)

    deduped: List[str] = []
    seen: Set[str] = set()
    for link in out:
        if link not in seen:
            seen.add(link)
            deduped.append(link)
    return deduped


def build_search_queries(component: Component, prefer_english: bool) -> List[str]:
    queries: List[str] = []
    part = component.manufacturer_part.strip()
    mfr = component.manufacturer.strip()
    lcsc = component.lcsc.strip()

    if part and mfr:
        queries.append(f'"{part}" "{mfr}" datasheet pdf')
    if part:
        queries.append(f'"{part}" datasheet pdf')
    if lcsc:
        queries.append(f'"{lcsc}" datasheet pdf')
    if part and lcsc:
        queries.append(f'"{part}" "{lcsc}" datasheet pdf')

    if prefer_english:
        queries = [f"{q} english" for q in queries]

    deduped: List[str] = []
    seen: Set[str] = set()
    for q in queries:
        if q not in seen:
            seen.add(q)
            deduped.append(q)
    return deduped


def resolve_pdf_url_from_candidate(
    candidate_url: str,
    component: Component,
    prefer_english: bool,
    visited: Optional[Set[str]] = None,
    deadline_ts: Optional[float] = None,
) -> Optional[str]:
    if deadline_ts is not None and time.time() > deadline_ts:
        return None
    if visited is None:
        visited = set()
    if candidate_url in visited:
        return None
    visited.add(candidate_url)

    try:
        final_url, headers, data = make_request(candidate_url, max_bytes=MAX_HTML_BYTES)
    except Exception:
        return None

    if is_pdf_response(final_url, headers, data[:8]):
        return final_url

    ctype = headers.get("content-type", "").lower()
    if "html" not in ctype and "text/" not in ctype:
        return None

    html_text = decode_response_content(data, headers)
    links = extract_links_from_html(html_text, final_url)
    links = sorted(
        links,
        key=lambda u: score_pdf_candidate(u, prefer_english=prefer_english),
        reverse=True,
    )

    tried = 0
    for link in links:
        if deadline_ts is not None and time.time() > deadline_ts:
            break
        if tried >= MAX_SEARCH_RESULTS_TO_TRY:
            break
        tried += 1
        try:
            l_final, l_headers, l_data = make_request(link, max_bytes=8192)
        except Exception:
            continue
        if is_pdf_response(l_final, l_headers, l_data):
            return l_final
    return None


def search_web_for_pdf(
    component: Component,
    prefer_english: bool,
    inspection_cache: Dict[str, Tuple[bool, str]],
    deadline_ts: Optional[float] = None,
) -> Optional[str]:
    for query in build_search_queries(component, prefer_english=prefer_english):
        if deadline_ts is not None and time.time() > deadline_ts:
            return None
        q = urllib.parse.urlencode({"q": query})
        search_url = f"https://duckduckgo.com/html/?{q}"
        try:
            final_url, headers, data = make_request(search_url, max_bytes=MAX_HTML_BYTES)
        except Exception:
            continue

        if "html" not in headers.get("content-type", "").lower():
            continue
        html_text = decode_response_content(data, headers)
        result_links = parse_search_results_duckduckgo(html_text)
        result_links = sorted(
            result_links,
            key=lambda u: score_pdf_candidate(u, prefer_english=prefer_english),
            reverse=True,
        )
        for link in result_links[:MAX_SEARCH_RESULTS_TO_TRY]:
            if deadline_ts is not None and time.time() > deadline_ts:
                return None
            pdf_url = resolve_pdf_url_from_candidate(
                link,
                component,
                prefer_english=prefer_english,
                deadline_ts=deadline_ts,
            )
            if pdf_url:
                ok, _reason = inspect_pdf_candidate(pdf_url, component, inspection_cache)
                if ok:
                    return pdf_url
    return None


def candidate_urls_for_component(component: Component) -> List[str]:
    candidates: List[str] = []
    if component.datasheet and looks_like_url(component.datasheet):
        candidates.append(component.datasheet)
    ti_url = build_ti_english_url(component)
    if ti_url:
        candidates.append(ti_url)

    # If we have an LCSC code, try obvious product URL patterns.
    if component.lcsc and re.fullmatch(r"C\d{3,}", component.lcsc, flags=re.IGNORECASE):
        code = component.lcsc.upper()
        candidates.append(f"https://www.lcsc.com/product-detail/{code}.html")
        candidates.append(f"https://item.szlcsc.com/{code}.html")

    deduped: List[str] = []
    seen: Set[str] = set()
    for c in candidates:
        url = normalize_url(c)
        if not url:
            continue
        if url not in seen:
            seen.add(url)
            deduped.append(url)
    return deduped


def choose_pdf_url(
    component: Component,
    inspection_cache: Dict[str, Tuple[bool, str]],
    allow_web_search: bool,
    mouser_api_key: str,
    mouser_cache: Dict[str, List[str]],
) -> Tuple[Optional[str], bool, str]:
    deadline_ts = time.time() + MAX_COMPONENT_RESOLUTION_SECONDS
    rejection_reasons: List[str] = []

    # Step 1: official distributor API lookup (Mouser) by MPN.
    if mouser_api_key and component.manufacturer_part:
        for api_candidate in get_mouser_datasheet_candidates(component, api_key=mouser_api_key, mouser_cache=mouser_cache):
            if time.time() > deadline_ts:
                return None, False, f"Timed out resolving datasheet after {MAX_COMPONENT_RESOLUTION_SECONDS}s"
            pdf_url = resolve_pdf_url_from_candidate(
                api_candidate,
                component,
                prefer_english=True,
                deadline_ts=deadline_ts,
            )
            if not pdf_url:
                continue
            ok, quality_reason = inspect_pdf_candidate(
                pdf_url,
                component,
                inspection_cache,
                strict_identity=False,
            )
            if ok:
                return pdf_url, False, "Resolved via Mouser API"
            rejection_reasons.append(f"{api_candidate} -> {quality_reason}")

    # Step 2: direct / crawled from known datasheet URLs and heuristics.
    for candidate in candidate_urls_for_component(component):
        if time.time() > deadline_ts:
            return None, False, f"Timed out resolving datasheet after {MAX_COMPONENT_RESOLUTION_SECONDS}s"
        pdf_url = resolve_pdf_url_from_candidate(
            candidate,
            component,
            prefer_english=False,
            deadline_ts=deadline_ts,
        )
        if pdf_url:
            ok, quality_reason = inspect_pdf_candidate(
                pdf_url,
                component,
                inspection_cache,
                strict_identity=False,
            )
            if not ok:
                rejection_reasons.append(f"{candidate} -> {quality_reason}")
                continue
            if likely_non_english_url(pdf_url) or likely_non_english_url(candidate):
                # Step 3: fallback search for English if source is likely non-English.
                english_pdf = None
                ti_url = build_ti_english_url(component)
                if ti_url:
                    candidate_english_pdf = resolve_pdf_url_from_candidate(
                        ti_url,
                        component,
                        prefer_english=True,
                        deadline_ts=deadline_ts,
                    )
                    if candidate_english_pdf:
                        ok, _reason = inspect_pdf_candidate(
                            candidate_english_pdf,
                            component,
                            inspection_cache,
                            strict_identity=False,
                        )
                        if ok:
                            english_pdf = candidate_english_pdf
                if not english_pdf:
                    if allow_web_search:
                        english_pdf = search_web_for_pdf(
                            component,
                            prefer_english=True,
                            inspection_cache=inspection_cache,
                            deadline_ts=deadline_ts,
                        )
                if english_pdf:
                    return english_pdf, True, "English fallback used"
            return pdf_url, False, "Resolved from project datasheet metadata"

    # Step 4: no direct hit, optionally do generic crawl/search.
    if not allow_web_search:
        if rejection_reasons:
            return None, False, "No acceptable datasheet found; rejected candidates: " + "; ".join(rejection_reasons[:4])
        return None, False, "No datasheet PDF URL found (web search disabled)"

    searched_pdf = search_web_for_pdf(
        component,
        prefer_english=False,
        inspection_cache=inspection_cache,
        deadline_ts=deadline_ts,
    )
    if searched_pdf:
        if likely_non_english_url(searched_pdf):
            english_pdf = search_web_for_pdf(
                component,
                prefer_english=True,
                inspection_cache=inspection_cache,
                deadline_ts=deadline_ts,
            )
            if english_pdf:
                return english_pdf, True, "Found via web search with English fallback"
        return searched_pdf, False, "Found via web search"

    if rejection_reasons:
        return None, False, "No acceptable datasheet found; rejected candidates: " + "; ".join(rejection_reasons[:4])
    return None, False, "No datasheet PDF URL found"


def download_pdf(url: str, destination_path: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as resp:
        data = resp.read()
        ctype = resp.headers.get("Content-Type", "").lower()
        if "application/pdf" not in ctype and not data.startswith(b"%PDF"):
            raise RuntimeError(f"URL did not return a PDF payload: {url}")
    ok, reason = evaluate_pdf_quality(url, data)
    if not ok:
        raise RuntimeError(reason)
    tmp = destination_path.with_suffix(destination_path.suffix + ".tmp")
    tmp.write_bytes(data)
    tmp.replace(destination_path)


def extract_components(project_root: Path) -> List[Component]:
    components: List[Component] = []
    for kicad_file in find_kicad_files(project_root):
        try:
            components.extend(extract_components_from_file(kicad_file))
        except Exception as exc:
            print(f"[WARN] Failed to parse {kicad_file}: {exc}", file=sys.stderr)
    deduped: List[Component] = []
    seen: Set[Tuple[str, ...]] = set()
    for component in components:
        key = component.unique_key()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(component)
    return deduped


def run(project_root: Path) -> int:
    datasheets_dir = project_root / "datasheets"
    datasheets_dir.mkdir(parents=True, exist_ok=True)

    components = extract_components(project_root)
    print(f"[INFO] Found {len(components)} unique component entries")
    print(f"[INFO] Web search enabled: {ENABLE_WEB_SEARCH_DEFAULT}")
    print(f"[INFO] Mouser API enabled: {bool(MOUSER_API_KEY_DEFAULT)}")
    if not MOUSER_API_KEY_DEFAULT:
        print("[INFO] Set DATASHEET_MOUSER_API_KEY to enable API-first datasheet lookup")

    downloaded_by_url: Dict[str, str] = {}
    inspection_cache: Dict[str, Tuple[bool, str]] = {}
    mouser_cache: Dict[str, List[str]] = {}
    success_count = 0
    skipped_count = 0
    failure_count = 0

    for idx, component in enumerate(components, start=1):
        label = component.label()
        print(f"[{idx}/{len(components)}] {label}")

        if component.reference.startswith("#"):
            skipped_count += 1
            print("  [SKIP] Power/virtual symbol")
            continue

        if not component.datasheet and not component.manufacturer_part and not component.lcsc:
            skipped_count += 1
            print("  [SKIP] No datasheet URL or part identifiers available")
            continue

        pdf_url, used_fallback, notes = choose_pdf_url(
            component,
            inspection_cache=inspection_cache,
            allow_web_search=ENABLE_WEB_SEARCH_DEFAULT,
            mouser_api_key=MOUSER_API_KEY_DEFAULT,
            mouser_cache=mouser_cache,
        )
        if not pdf_url:
            failure_count += 1
            print(f"  [FAIL] {notes}")
            continue

        if pdf_url in downloaded_by_url:
            output_path = downloaded_by_url[pdf_url]
            success_count += 1
            suffix = " (english fallback)" if used_fallback else ""
            print(f"  [OK] Reused {output_path}{suffix}")
            continue

        filename = f"{safe_slug(label)}_{hashlib.sha1(pdf_url.encode('utf-8')).hexdigest()[:10]}.pdf"
        destination = datasheets_dir / filename
        try:
            download_pdf(pdf_url, destination)
            downloaded_by_url[pdf_url] = str(destination)
            success_count += 1
            suffix = " (english fallback)" if used_fallback else ""
            print(f"  [OK] Saved {destination}{suffix}")
            time.sleep(0.12)
        except Exception as exc:
            failure_count += 1
            print(f"  [FAIL] Download error: {exc}")

    print("")
    print("[DONE]")
    print(f"  Output folder : {datasheets_dir}")
    print(f"  Downloaded    : {success_count}")
    print(f"  Skipped       : {skipped_count}")
    print(f"  Failed        : {failure_count}")
    return 0 if success_count > 0 else 1


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir
    return run(project_root)


if __name__ == "__main__":
    raise SystemExit(main())
