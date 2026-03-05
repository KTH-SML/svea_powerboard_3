#!/usr/bin/env python3
"""
Download datasheets for components found in either:
- KiCad schematic files under a project directory, or
- One or more BOM CSV files (for example JLCPCB exports).

Default behavior:
- Assumes this script is placed in the KiCad project root directory.
- Scans all `.kicad_sch` files in that directory recursively.
- Extracts component metadata (Datasheet URL, MPN, Manufacturer, LCSC code, etc.).
- Downloads datasheets into `./datasheets`.
- If a datasheet source appears non-English, attempts to find an English fallback.
- Prints status directly to stdout.
"""

from __future__ import annotations

import argparse
import csv
import dataclasses
import hashlib
import html
import os
import json
import re
import shutil
import subprocess
import sys
import tempfile
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
CURL_BIN = shutil.which("curl")

REQUEST_TIMEOUT_SECONDS = max(5, int(os.getenv("DATASHEET_REQUEST_TIMEOUT_SECONDS", "25")))
REQUEST_RETRY_COUNT = max(0, int(os.getenv("DATASHEET_REQUEST_RETRY_COUNT", "2")))
REQUEST_RETRY_BACKOFF_SECONDS = max(0.0, float(os.getenv("DATASHEET_REQUEST_RETRY_BACKOFF_SECONDS", "1.0")))
MAX_HTML_BYTES = 1_500_000
MAX_SEARCH_RESULTS_TO_TRY = 8
MAX_PDF_INSPECTION_BYTES = 2_500_000
MAX_COMPONENT_RESOLUTION_SECONDS = max(8, int(os.getenv("DATASHEET_COMPONENT_TIMEOUT_SECONDS", "18")))
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
    "lcsc datasheet notice",
    "datasheet notice",
    "datasheet temporarily unavailable",
    "datasheet unavailable",
    "document unavailable",
    "file unavailable",
    "temporarily unavailable",
    "no datasheet",
    "not found",
    "404 not found",
    "error 404",
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

BAD_PDF_URL_HINTS = (
    "download-iso9001-certification",
    "iso9001",
    "iso-iec",
    "certificate.pdf",
    "certification.pdf",
    "quality-assurance",
)

IDENTIFIER_SPLIT_RE = re.compile(r"[\s,;/|()\\]+")
NON_ALNUM_RE = re.compile(r"[^A-Za-z0-9]+")
HEADER_NORMALIZE_RE = re.compile(r"[^a-z0-9]+")
CJK_CHAR_RE = re.compile(r"[\u4e00-\u9fff]")
ENGLISH_WORD_RE = re.compile(r"[A-Za-z]{3,}")
PDFTOTEXT_BIN = shutil.which("pdftotext")

CSV_ALIASES = {
    "datasheet": [
        "datasheet",
        "datasheet url",
        "datasheet link",
    ],
    "manufacturer": [
        "manufacturer",
        "mfr",
        "brand",
    ],
    "manufacturer_part": [
        "manufacturer part",
        "manufacturer part number",
        "manufacturer pn",
        "mpn",
        "part number",
        "part no",
    ],
    "lcsc": [
        "lcsc",
        "lcsc part",
        "lcsc part #",
        "jlcpcb part",
        "jlcpcb part #",
        "jlcpcb",
    ],
    "description": [
        "description",
        "comment",
        "value",
        "name",
    ],
    "reference": [
        "designator",
        "reference",
        "refdes",
        "refs",
    ],
    "symbol_name": [
        "footprint",
        "package",
        "symbol",
    ],
    "value": [
        "comment",
        "value",
    ],
}


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


def parse_curl_headers(header_blob: str) -> Dict[str, str]:
    # curl can include one header block per redirect. Keep the last real response block.
    blocks = re.split(r"\r?\n\r?\n", header_blob.strip())
    for block in reversed(blocks):
        lines = [line.strip("\r") for line in block.splitlines() if line.strip()]
        if not lines:
            continue
        headers: Dict[str, str] = {}
        for line in lines[1:]:
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            headers[key.strip().lower()] = value.strip()
        if headers:
            return headers
    return {}


def make_request_with_curl(url: str, max_bytes: Optional[int] = None) -> Tuple[str, Dict[str, str], bytes]:
    if not CURL_BIN:
        raise RuntimeError("curl binary not found")

    with tempfile.TemporaryDirectory(prefix="datasheet-curl-") as tmpdir:
        tmp_path = Path(tmpdir)
        header_path = tmp_path / "headers.txt"
        body_path = tmp_path / "body.bin"
        cmd = [
            CURL_BIN,
            "-L",
            "--silent",
            "--show-error",
            "--fail",
            "--max-time",
            str(max(5, REQUEST_TIMEOUT_SECONDS)),
            "-A",
            USER_AGENT,
            "-D",
            str(header_path),
            "-o",
            str(body_path),
            "-w",
            "%{url_effective}",
            url,
        ]
        if max_bytes is not None and max_bytes > 0:
            cmd.extend(["--range", f"0-{max_bytes - 1}"])

        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            timeout=REQUEST_TIMEOUT_SECONDS + 8,
        )
        if proc.returncode != 0:
            detail = (proc.stderr or proc.stdout or "").strip()
            raise RuntimeError(f"curl request failed (exit {proc.returncode}): {detail}")

        final_url = (proc.stdout or "").strip() or url
        headers_text = header_path.read_text(encoding="latin1", errors="ignore") if header_path.exists() else ""
        headers = parse_curl_headers(headers_text)
        data = body_path.read_bytes() if body_path.exists() else b""
        if max_bytes is not None and len(data) > max_bytes:
            data = data[:max_bytes]
        return final_url, headers, data


def make_request(url: str, max_bytes: Optional[int] = None) -> Tuple[str, Dict[str, str], bytes]:
    last_error: Optional[Exception] = None
    for attempt in range(REQUEST_RETRY_COUNT + 1):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as resp:
                final_url = resp.geturl()
                headers = {k.lower(): v for k, v in resp.headers.items()}
                if max_bytes is None:
                    data = resp.read()
                else:
                    data = resp.read(max_bytes)
                return final_url, headers, data
        except Exception as exc:
            last_error = exc
            if attempt >= REQUEST_RETRY_COUNT:
                break
            sleep_seconds = REQUEST_RETRY_BACKOFF_SECONDS * (attempt + 1)
            if sleep_seconds > 0:
                time.sleep(sleep_seconds)

    if CURL_BIN:
        try:
            return make_request_with_curl(url, max_bytes=max_bytes)
        except Exception as exc:
            last_error = exc if last_error is None else RuntimeError(f"{last_error}; curl fallback failed: {exc}")
    assert last_error is not None
    raise last_error


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
ESCAPED_PDF_URL_RE = re.compile(r'https:\\u002F\\u002F[^\s"\'<>]+?\.pdf(?:\\u003F[^\s"\'<>]*)?', re.IGNORECASE)


def decode_js_escaped_url(value: str) -> str:
    # LCSC pages often embed datasheet URLs in escaped JSON strings.
    value = value.replace("\\/", "/")
    value = value.replace("\\u002F", "/")
    value = value.replace("\\u003A", ":")
    value = value.replace("\\u003F", "?")
    value = value.replace("\\u0026", "&")
    value = value.replace("\\u003D", "=")
    return value


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
    for raw in ESCAPED_PDF_URL_RE.findall(html_text):
        decoded = decode_js_escaped_url(raw)
        if looks_like_url(decoded):
            links.append(decoded)

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
    if "datasheet.lcsc.com" in lurl:
        score += 25
    if lurl.endswith(".pdf") or ".pdf?" in lurl:
        score += 10
    if "datasheet" in lurl:
        score += 5
    if "download" in lurl:
        score += 2
    if "search?" in lurl or "bing.com/search" in lurl or "google." in lurl:
        score -= 8
    if any(hint in lurl for hint in BAD_PDF_URL_HINTS):
        score -= 35
    if likely_non_english_url(url):
        score -= 6 if prefer_english else 1
    if prefer_english and any(x in lurl for x in ("/en/", "lang=en", "locale=en")):
        score += 4
    return score


def score_pdf_candidate_for_component(url: str, component: "Component", prefer_english: bool) -> int:
    score = score_pdf_candidate(url, prefer_english=prefer_english)
    url_id = normalize_identifier(urllib.parse.unquote(url))
    identifiers = component_identifiers(component)
    matches = [ident for ident in identifiers if ident in url_id]
    if matches:
        score += 12 + min(3, len(matches)) * 4
    elif identifiers:
        score -= 4
    return score


def is_generic_non_datasheet_pdf_url(url: str) -> bool:
    lurl = url.lower()
    return any(hint in lurl for hint in BAD_PDF_URL_HINTS)


def is_pdf_response(url: str, headers: Dict[str, str], data_prefix: bytes) -> bool:
    ctype = headers.get("content-type", "").lower()
    if "application/pdf" in ctype:
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


def extract_pdf_text_with_pdftotext(data: bytes) -> str:
    if not PDFTOTEXT_BIN:
        return ""

    pdf_path = None
    txt_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_tmp:
            pdf_tmp.write(data)
            pdf_path = pdf_tmp.name
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as txt_tmp:
            txt_path = txt_tmp.name

        subprocess.run(
            [PDFTOTEXT_BIN, "-f", "1", "-l", "2", "-enc", "UTF-8", pdf_path, txt_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=15,
        )

        if not txt_path or not os.path.exists(txt_path):
            return ""
        try:
            text = Path(txt_path).read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return ""
        return text.lower()
    except Exception:
        return ""
    finally:
        for path in (pdf_path, txt_path):
            if path and os.path.exists(path):
                try:
                    os.unlink(path)
                except Exception:
                    pass


def pdf_text_looks_non_english(text: str) -> bool:
    if not text:
        return False
    cjk_chars = len(CJK_CHAR_RE.findall(text))
    english_words = len(ENGLISH_WORD_RE.findall(text))
    return cjk_chars >= 40 and cjk_chars > english_words


def is_pdf_likely_non_english(url: str, language_cache: Dict[str, bool]) -> bool:
    if url in language_cache:
        return language_cache[url]

    result = False
    try:
        final_url, headers, data = make_request(url, max_bytes=MAX_PDF_INSPECTION_BYTES)
        if is_pdf_response(final_url, headers, data[:8]):
            if likely_non_english_url(final_url):
                result = True
            else:
                text = extract_pdf_text_with_pdftotext(data)
                result = pdf_text_looks_non_english(text)
    except Exception:
        result = False

    language_cache[url] = result
    return result


def normalize_identifier(value: str) -> str:
    return NON_ALNUM_RE.sub("", value or "").upper()


def looks_like_part_number(value: str) -> bool:
    cleaned = normalize_identifier(value)
    if len(cleaned) < 6:
        return False
    has_alpha = any(ch.isalpha() for ch in cleaned)
    has_digit = any(ch.isdigit() for ch in cleaned)
    return has_alpha and has_digit


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

    value = component.value.strip()
    if value and looks_like_part_number(value):
        add(value)
        for piece in IDENTIFIER_SPLIT_RE.split(value):
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
    ltext = html_text.lower()
    if "bots use duckduckgo too" in ltext or "anomaly-modal" in ltext:
        return []

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
    value = component.value.strip()

    if part and mfr:
        queries.append(f'"{part}" "{mfr}" datasheet pdf')
    if part:
        queries.append(f'"{part}" datasheet pdf')
    if value and looks_like_part_number(value):
        queries.append(f'"{value}" datasheet pdf')
        if mfr:
            queries.append(f'"{value}" "{mfr}" datasheet pdf')
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
        key=lambda u: score_pdf_candidate_for_component(u, component, prefer_english=prefer_english),
        reverse=True,
    )

    tried = 0
    for link in links:
        if deadline_ts is not None and time.time() > deadline_ts:
            break
        if tried >= MAX_SEARCH_RESULTS_TO_TRY:
            break
        if is_generic_non_datasheet_pdf_url(link):
            continue
        tried += 1
        try:
            l_final, l_headers, l_data = make_request(link, max_bytes=8192)
        except Exception:
            continue
        if is_pdf_response(l_final, l_headers, l_data):
            if is_generic_non_datasheet_pdf_url(l_final):
                continue
            return l_final
    return None


def search_web_for_pdf(
    component: Component,
    prefer_english: bool,
    inspection_cache: Dict[str, Tuple[bool, str]],
    strict_identity: bool = True,
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
            key=lambda u: score_pdf_candidate_for_component(u, component, prefer_english=prefer_english),
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
                ok, _reason = inspect_pdf_candidate(
                    pdf_url,
                    component,
                    inspection_cache,
                    strict_identity=strict_identity,
                )
                if ok:
                    return pdf_url
    return None


def candidate_urls_for_component(component: Component) -> List[str]:
    candidates: List[str] = []
    if component.lcsc and re.fullmatch(r"C\d{3,}", component.lcsc, flags=re.IGNORECASE):
        code = component.lcsc.upper()
        # Modern LCSC direct datasheet endpoint by part code.
        candidates.append(f"https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/{code}.pdf")
        # LCSC datasheet landing page, which embeds current PDF URLs.
        candidates.append(f"https://www.lcsc.com/datasheet/{code}.pdf")

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
    language_cache: Dict[str, bool],
    english_only: bool,
    allow_web_search: bool,
    mouser_api_key: str,
    mouser_cache: Dict[str, List[str]],
) -> Tuple[Optional[str], bool, str]:
    deadline_ts = time.time() + MAX_COMPONENT_RESOLUTION_SECONDS
    rejection_reasons: List[str] = []
    trusted_datasheet_url = normalize_url(component.datasheet)

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
                strict_identity=True,
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
            candidate_is_trusted = bool(trusted_datasheet_url) and normalize_url(candidate) == trusted_datasheet_url
            ok, quality_reason = inspect_pdf_candidate(
                pdf_url,
                component,
                inspection_cache,
                strict_identity=not candidate_is_trusted,
            )
            if not ok:
                rejection_reasons.append(f"{candidate} -> {quality_reason}")
                continue
            if (
                likely_non_english_url(pdf_url)
                or likely_non_english_url(candidate)
                or is_pdf_likely_non_english(pdf_url, language_cache)
            ):
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
                            strict_identity=True,
                        )
                        if ok:
                            english_pdf = candidate_english_pdf
                if not english_pdf:
                    if allow_web_search:
                        english_pdf = search_web_for_pdf(
                            component,
                            prefer_english=True,
                            inspection_cache=inspection_cache,
                            strict_identity=False,
                            deadline_ts=deadline_ts,
                        )
                if english_pdf:
                    return english_pdf, True, "English fallback used"
                if english_only:
                    return None, False, "Rejected non-English datasheet (english-only mode)"
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
        strict_identity=True,
        deadline_ts=deadline_ts,
    )
    if searched_pdf:
        if likely_non_english_url(searched_pdf):
            english_pdf = search_web_for_pdf(
                component,
                prefer_english=True,
                inspection_cache=inspection_cache,
                strict_identity=False,
                deadline_ts=deadline_ts,
            )
            if english_pdf:
                return english_pdf, True, "Found via web search with English fallback"
        return searched_pdf, False, "Found via web search"

    if rejection_reasons:
        return None, False, "No acceptable datasheet found; rejected candidates: " + "; ".join(rejection_reasons[:4])
    return None, False, "No datasheet PDF URL found"


def download_pdf(url: str, destination_path: Path) -> None:
    _final_url, headers, data = make_request(url, max_bytes=None)
    ctype = headers.get("content-type", "").lower()
    if "application/pdf" not in ctype and not data.startswith(b"%PDF"):
        raise RuntimeError(f"URL did not return a PDF payload: {url}")
    ok, reason = evaluate_pdf_quality(url, data)
    if not ok:
        raise RuntimeError(reason)
    tmp = destination_path.with_suffix(destination_path.suffix + ".tmp")
    tmp.write_bytes(data)
    tmp.replace(destination_path)


def build_output_filename(component: Component, pdf_url: str) -> str:
    parts: List[str] = []
    for raw in (component.value, component.manufacturer_part, component.lcsc):
        value = (raw or "").strip()
        if not value or is_placeholder(value):
            continue
        slug = safe_slug(value, max_len=42)
        if slug and slug not in parts:
            parts.append(slug)
    if not parts:
        parts.append(safe_slug(component.label(), max_len=80))
    stem = "_".join(parts[:3])
    digest = hashlib.sha1(pdf_url.encode("utf-8")).hexdigest()[:10]
    return f"{stem}_{digest}.pdf"


def normalize_header_name(name: str) -> str:
    return HEADER_NORMALIZE_RE.sub("", (name or "").strip().lower())


def get_csv_field(row: Dict[str, str], aliases: List[str]) -> str:
    normalized_row = {normalize_header_name(k): (v or "").strip() for k, v in row.items() if k is not None}
    for alias in aliases:
        value = normalized_row.get(normalize_header_name(alias), "")
        if value and not is_placeholder(value):
            return value
    return ""


def normalize_lcsc(value: str) -> str:
    value = value.strip().upper()
    if not value:
        return ""
    if re.fullmatch(r"C\d{3,}", value):
        return value
    if value.isdigit():
        return f"C{value}"
    return value


def extract_components_from_csv(path: Path) -> List[Component]:
    components: List[Component] = []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            datasheet = get_csv_field(row, CSV_ALIASES["datasheet"])
            manufacturer = get_csv_field(row, CSV_ALIASES["manufacturer"])
            manufacturer_part = get_csv_field(row, CSV_ALIASES["manufacturer_part"])
            lcsc = normalize_lcsc(get_csv_field(row, CSV_ALIASES["lcsc"]))
            description = get_csv_field(row, CSV_ALIASES["description"])
            reference = get_csv_field(row, CSV_ALIASES["reference"])
            symbol_name = get_csv_field(row, CSV_ALIASES["symbol_name"])
            value = get_csv_field(row, CSV_ALIASES["value"]) or description

            if not datasheet and not manufacturer_part and not lcsc:
                continue

            components.append(
                Component(
                    source_file=str(path),
                    source_kind="bom_csv",
                    symbol_name=symbol_name,
                    reference=reference,
                    value=value,
                    datasheet=datasheet,
                    manufacturer=manufacturer,
                    manufacturer_part=manufacturer_part,
                    lcsc=lcsc,
                    description=description,
                )
            )
    return components


def extract_components(project_root: Path, csv_paths: Optional[List[Path]] = None) -> List[Component]:
    components: List[Component] = []
    if csv_paths:
        for csv_path in csv_paths:
            try:
                components.extend(extract_components_from_csv(csv_path))
            except Exception as exc:
                print(f"[WARN] Failed to parse CSV {csv_path}: {exc}", file=sys.stderr)
    else:
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


def local_component_enrichment_score(component: Component) -> int:
    score = 0
    if normalize_url(component.datasheet):
        score += 4
    if component.manufacturer_part and not is_placeholder(component.manufacturer_part):
        score += 3
    if component.manufacturer and not is_placeholder(component.manufacturer):
        score += 2
    return score


def build_local_lcsc_component_index(project_root: Path) -> Dict[str, Component]:
    index: Dict[str, Component] = {}
    for component in extract_components(project_root, csv_paths=None):
        code = normalize_lcsc(component.lcsc)
        if not code:
            continue
        if code not in index:
            index[code] = component
            continue
        if local_component_enrichment_score(component) > local_component_enrichment_score(index[code]):
            index[code] = component
    return index


def run(
    project_root: Path,
    csv_paths: Optional[List[Path]] = None,
    datasheets_dir_override: Optional[Path] = None,
    allow_web_search: Optional[bool] = None,
    mouser_api_key: Optional[str] = None,
    english_only: bool = False,
) -> int:
    datasheets_dir = datasheets_dir_override or (project_root / "datasheets")
    datasheets_dir.mkdir(parents=True, exist_ok=True)

    components = extract_components(project_root, csv_paths=csv_paths)
    resolved_allow_web_search = ENABLE_WEB_SEARCH_DEFAULT if allow_web_search is None else allow_web_search
    resolved_mouser_api_key = MOUSER_API_KEY_DEFAULT if mouser_api_key is None else mouser_api_key.strip()
    local_lcsc_component_index: Dict[str, Component] = {}
    if csv_paths:
        local_lcsc_component_index = build_local_lcsc_component_index(project_root)

    print(f"[INFO] Found {len(components)} unique component entries")
    print(f"[INFO] Web search enabled: {resolved_allow_web_search}")
    print(f"[INFO] Mouser API enabled: {bool(resolved_mouser_api_key)}")
    print(f"[INFO] HTTP timeout: {REQUEST_TIMEOUT_SECONDS}s (retries: {REQUEST_RETRY_COUNT})")
    if csv_paths:
        print(f"[INFO] CSV mode: {len(csv_paths)} file(s)")
        print(f"[INFO] Local LCSC component mappings: {len(local_lcsc_component_index)}")
    else:
        print(f"[INFO] KiCad mode: scanning {project_root}")

    if not resolved_mouser_api_key:
        print("[INFO] Set DATASHEET_MOUSER_API_KEY to enable API-first datasheet lookup")

    downloaded_by_url: Dict[str, str] = {}
    inspection_cache: Dict[str, Tuple[bool, str]] = {}
    language_cache: Dict[str, bool] = {}
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

        if csv_paths and not component.datasheet and component.lcsc:
            mapped_component = local_lcsc_component_index.get(normalize_lcsc(component.lcsc))
            if mapped_component:
                if not component.datasheet and normalize_url(mapped_component.datasheet):
                    component.datasheet = mapped_component.datasheet
                if not component.manufacturer_part and not is_placeholder(mapped_component.manufacturer_part):
                    component.manufacturer_part = mapped_component.manufacturer_part
                if not component.manufacturer and not is_placeholder(mapped_component.manufacturer):
                    component.manufacturer = mapped_component.manufacturer

        if not component.datasheet and not component.manufacturer_part and not component.lcsc:
            skipped_count += 1
            print("  [SKIP] No datasheet URL or part identifiers available")
            continue

        pdf_url, used_fallback, notes = choose_pdf_url(
            component,
            inspection_cache=inspection_cache,
            language_cache=language_cache,
            english_only=english_only,
            allow_web_search=resolved_allow_web_search,
            mouser_api_key=resolved_mouser_api_key,
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

        filename = build_output_filename(component, pdf_url)
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


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download component datasheets from KiCad schematics or BOM CSV files.")
    parser.add_argument(
        "--csv",
        dest="csv_paths",
        action="append",
        default=[],
        help="Path to a BOM CSV file. Can be passed multiple times.",
    )
    parser.add_argument(
        "--project-root",
        default=None,
        help="Project root to scan for .kicad_sch files (default: script directory). Ignored when --csv is used.",
    )
    parser.add_argument(
        "--datasheets-dir",
        default=None,
        help="Output directory for downloaded PDFs (default: <project-root>/datasheets).",
    )
    parser.add_argument(
        "--web-search",
        action="store_true",
        help="Enable web-search fallback for unresolved parts.",
    )
    parser.add_argument(
        "--english-only",
        action="store_true",
        help="Reject non-English PDFs when no English fallback is found.",
    )
    parser.add_argument(
        "--mouser-api-key",
        default=None,
        help="Mouser API key to use for API-first datasheet lookup.",
    )
    return parser.parse_args(argv)


def main() -> int:
    args = parse_args()
    script_dir = Path(__file__).resolve().parent

    project_root = Path(args.project_root).expanduser().resolve() if args.project_root else script_dir
    csv_paths = [Path(p).expanduser().resolve() for p in args.csv_paths]
    for csv_path in csv_paths:
        if not csv_path.is_file():
            print(f"[ERROR] CSV path does not exist or is not a file: {csv_path}", file=sys.stderr)
            return 2

    datasheets_dir = Path(args.datasheets_dir).expanduser().resolve() if args.datasheets_dir else None
    allow_web_search = ENABLE_WEB_SEARCH_DEFAULT or args.web_search

    return run(
        project_root=project_root,
        csv_paths=csv_paths or None,
        datasheets_dir_override=datasheets_dir,
        allow_web_search=allow_web_search,
        mouser_api_key=args.mouser_api_key,
        english_only=args.english_only,
    )


if __name__ == "__main__":
    raise SystemExit(main())
