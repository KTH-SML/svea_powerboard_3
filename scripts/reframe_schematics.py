#!/usr/bin/env python3
import glob
import os
import re
from datetime import date

ROOT = "/Users/nils/Downloads/tryingkicadimport"
MARGIN_MM = 20.0
MIN_W = 297.0
MIN_H = 210.0
TODAY = date(2026, 2, 16).isoformat()

DRAWING_LIB_RE = re.compile(r"^5v rail sm-easyedapro:Drawing-Symbol_")


def block_end(lines, start):
    depth = 0
    i = start
    while i < len(lines):
        depth += lines[i].count("(") - lines[i].count(")")
        if depth == 0:
            return i
        i += 1
    return len(lines) - 1


def find_lib_symbols_bounds(lines):
    for i, line in enumerate(lines):
        if line.strip() == "(lib_symbols":
            return i, block_end(lines, i)
    return None, None


def parse_symbol_name(symbol_line):
    s = symbol_line.strip()
    if not s.startswith('(symbol "'):
        return None
    return s[len('(symbol "') :].split('"', 1)[0]


def is_drawing_symbol_lib_block(block_lines):
    name = parse_symbol_name(block_lines[0])
    return bool(name and DRAWING_LIB_RE.match(name))


def is_drawing_symbol_instance(block_text):
    m = re.search(r'\(lib_id "([^"]+)"\)', block_text)
    return bool(m and DRAWING_LIB_RE.match(m.group(1)))


def remove_drawing_blocks(lines):
    lib_start, lib_end = find_lib_symbols_bounds(lines)
    if lib_start is None:
        return lines, 0, 0

    removed_lib_defs = 0
    removed_instances = 0

    # 1) Remove drawing symbol definitions from lib_symbols
    lib_lines = lines[lib_start : lib_end + 1]
    i = 0
    while i < len(lib_lines):
        if lib_lines[i].strip().startswith('(symbol "'):
            j = block_end(lib_lines, i)
            block = lib_lines[i : j + 1]
            if is_drawing_symbol_lib_block(block):
                del lib_lines[i : j + 1]
                removed_lib_defs += 1
                continue
            i = j + 1
        else:
            i += 1

    lines = lines[:lib_start] + lib_lines + lines[lib_end + 1 :]

    # 2) Remove drawing symbol instances from top-level schematic items
    i = 0
    while i < len(lines):
        if lines[i].strip() == "(symbol":
            j = block_end(lines, i)
            block_text = "\n".join(lines[i : j + 1])
            if is_drawing_symbol_instance(block_text):
                del lines[i : j + 1]
                removed_instances += 1
                continue
            i = j + 1
        else:
            i += 1

    return lines, removed_lib_defs, removed_instances


def sheet_title_from_name(path):
    name = os.path.basename(path).replace(".kicad_sch", "")
    if "_" in name:
        left, right = name.split("_", 1)
        if left.isdigit():
            return right
    return name


def add_or_replace_title_block(lines, title):
    # remove existing title_block if any
    i = 0
    while i < len(lines):
        if lines[i].strip() == "(title_block":
            j = block_end(lines, i)
            del lines[i : j + 1]
            continue
        i += 1

    insert_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith("(paper "):
            insert_idx = i + 1
            break
    if insert_idx is None:
        insert_idx = 6

    block = [
        "\t(title_block",
        f'\t\t(title "{title}")',
        f'\t\t(date "{TODAY}")',
        '\t\t(company "")',
        "\t)",
    ]
    lines[insert_idx:insert_idx] = block
    return lines


def extract_schematic_region(lines):
    lib_start, lib_end = find_lib_symbols_bounds(lines)
    if lib_start is None:
        return "\n".join(lines), (0, len(lines))
    pre = "\n".join(lines[:lib_start])
    post = "\n".join(lines[lib_end + 1 :])
    return post, (lib_start, lib_end)


def compute_bbox_from_text(text):
    patterns = [
        r"\(at\s+(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)",
        r"\(xy\s+(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)",
        r"\(start\s+(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)",
        r"\(end\s+(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)",
        r"\(center\s+(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)",
        r"\(mid\s+(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)",
    ]
    xs = []
    ys = []
    for pat in patterns:
        for m in re.finditer(pat, text):
            xs.append(float(m.group(1)))
            ys.append(float(m.group(2)))
    if not xs:
        return None
    return min(xs), min(ys), max(xs), max(ys)


def fmt_num(v):
    s = f"{v:.4f}".rstrip("0").rstrip(".")
    return s if s else "0"


def shift_coords(text, dx, dy):
    def repl(prefix, match):
        x = float(match.group(2)) + dx
        y = float(match.group(4)) + dy
        return f"{match.group(1)}{fmt_num(x)}{match.group(3)}{fmt_num(y)}"

    patterns = [
        r"(\(at\s+)(-?\d+(?:\.\d+)?)(\s+)(-?\d+(?:\.\d+)?)",
        r"(\(xy\s+)(-?\d+(?:\.\d+)?)(\s+)(-?\d+(?:\.\d+)?)",
        r"(\(start\s+)(-?\d+(?:\.\d+)?)(\s+)(-?\d+(?:\.\d+)?)",
        r"(\(end\s+)(-?\d+(?:\.\d+)?)(\s+)(-?\d+(?:\.\d+)?)",
        r"(\(center\s+)(-?\d+(?:\.\d+)?)(\s+)(-?\d+(?:\.\d+)?)",
        r"(\(mid\s+)(-?\d+(?:\.\d+)?)(\s+)(-?\d+(?:\.\d+)?)",
    ]
    out = text
    for pat in patterns:
        out = re.sub(pat, lambda m: repl(pat, m), out)
    return out


def set_paper_user(lines, width, height):
    paper_line = f'\t(paper "User" {fmt_num(width)} {fmt_num(height)})'
    for i, line in enumerate(lines):
        if line.strip().startswith("(paper "):
            lines[i] = paper_line
            return lines
    lines.insert(5, paper_line)
    return lines


def process_file(path):
    original = open(path, "r", encoding="utf-8").read()
    lines = original.splitlines()

    lines, lib_defs_removed, instances_removed = remove_drawing_blocks(lines)

    # Recompute bbox from non-lib schematic section only
    post_text, (lib_start, lib_end) = extract_schematic_region(lines)
    bbox = compute_bbox_from_text(post_text)

    recentered = False
    if bbox:
        minx, miny, maxx, maxy = bbox
        content_w = maxx - minx
        content_h = maxy - miny

        width = max(MIN_W, content_w + 2 * MARGIN_MM)
        height = max(MIN_H, content_h + 2 * MARGIN_MM)

        current_cx = (minx + maxx) / 2.0
        current_cy = (miny + maxy) / 2.0
        target_cx = width / 2.0
        target_cy = height / 2.0
        dx = target_cx - current_cx
        dy = target_cy - current_cy

        if abs(dx) > 1e-6 or abs(dy) > 1e-6:
            # shift only non-lib section
            pre_lines = lines[: lib_end + 1]
            post_lines = lines[lib_end + 1 :]
            post_shifted = shift_coords("\n".join(post_lines), dx, dy).split("\n")
            lines = pre_lines + post_shifted
            recentered = True

        lines = set_paper_user(lines, width, height)

    title = sheet_title_from_name(path)
    lines = add_or_replace_title_block(lines, title)

    updated = "\n".join(lines)
    if original.endswith("\n"):
        updated += "\n"

    if updated != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(updated)
        return {
            "changed": True,
            "lib_defs_removed": lib_defs_removed,
            "instances_removed": instances_removed,
            "recentered": recentered,
        }

    return {
        "changed": False,
        "lib_defs_removed": 0,
        "instances_removed": 0,
        "recentered": False,
    }


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "*.kicad_sch")))
    changed = 0
    total_defs = 0
    total_instances = 0
    total_recentered = 0

    for p in files:
        res = process_file(p)
        if res["changed"]:
            changed += 1
            total_defs += res["lib_defs_removed"]
            total_instances += res["instances_removed"]
            total_recentered += int(res["recentered"])
            print(
                f"{os.path.basename(p)}: frame defs -{res['lib_defs_removed']}, "
                f"frame instances -{res['instances_removed']}, recentered={res['recentered']}"
            )

    print(f"\nFiles updated: {changed}")
    print(f"Drawing symbol defs removed: {total_defs}")
    print(f"Drawing symbol instances removed: {total_instances}")
    print(f"Sheets recentered: {total_recentered}")


if __name__ == "__main__":
    main()
