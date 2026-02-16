#!/usr/bin/env python3
import math
import re
from datetime import date

PARENT = "/Users/nils/Downloads/tryingkicadimport/5v rail smart enable.kicad_sch"
TODAY = date(2026, 2, 16).isoformat()

# Layout tuning
COLS = 3
X0 = 10.0
Y0 = 15.0
STEP_X = 92.0
STEP_Y = 26.0
SHEET_W = 82.0
SHEET_H = 18.0


def fmt_num(v: float) -> str:
    s = f"{v:.4f}".rstrip("0").rstrip(".")
    return s if s else "0"


def paren_delta_ignoring_quotes(line: str) -> int:
    in_quote = False
    escaped = False
    delta = 0
    for ch in line:
        if escaped:
            escaped = False
            continue
        if ch == "\\" and in_quote:
            escaped = True
            continue
        if ch == '"':
            in_quote = not in_quote
            continue
        if not in_quote:
            if ch == '(':
                delta += 1
            elif ch == ')':
                delta -= 1
    return delta


def block_end(lines, start):
    depth = 0
    i = start
    while i < len(lines):
        depth += paren_delta_ignoring_quotes(lines[i])
        if depth == 0:
            return i
        i += 1
    return len(lines) - 1


def parse_page_num(sheet_text: str):
    m = re.search(r'\(page "([^"]+)"\)', sheet_text)
    if not m:
        return 9999, ""
    raw = m.group(1)
    try:
        return int(raw), raw
    except ValueError:
        return 9999, raw


def set_line_value(line: str, key: str, values):
    indent = line[: len(line) - len(line.lstrip())]
    vals = " ".join(values)
    return f"{indent}({key} {vals})"


def update_sheet_block(block_lines, at_x, at_y):
    lines = block_lines[:]

    # 1) top-level (at ...) and (size ...)
    seen_property = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('(property '):
            seen_property = True
        if not seen_property and stripped.startswith('(at '):
            lines[i] = set_line_value(line, 'at', [fmt_num(at_x), fmt_num(at_y)])
            break

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('(size '):
            lines[i] = set_line_value(line, 'size', [fmt_num(SHEET_W), fmt_num(SHEET_H)])
            break

    # 2) Sheetname and Sheetfile property positions
    for i, line in enumerate(lines):
        stripped = line.strip()
        if '(property "Sheetname"' in stripped:
            for j in range(i + 1, min(i + 8, len(lines))):
                if lines[j].strip().startswith('(at '):
                    lines[j] = set_line_value(lines[j], 'at', [fmt_num(at_x), fmt_num(at_y - 0.7116), '0'])
                    break
        if '(property "Sheetfile"' in stripped:
            for j in range(i + 1, min(i + 8, len(lines))):
                if lines[j].strip().startswith('(at '):
                    lines[j] = set_line_value(lines[j], 'at', [fmt_num(at_x), fmt_num(at_y + SHEET_H + 0.5846), '0'])
                    break

    return lines


def update_title_and_paper(lines, total_sheets):
    rows = math.ceil(total_sheets / COLS)
    width = X0 * 2 + (COLS - 1) * STEP_X + SHEET_W
    height = Y0 * 2 + (rows - 1) * STEP_Y + SHEET_H

    for i, line in enumerate(lines):
        if line.strip().startswith('(paper '):
            indent = line[: len(line) - len(line.lstrip())]
            lines[i] = f'{indent}(paper "User" {fmt_num(width)} {fmt_num(height)})'
            break

    in_title_block = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == '(title_block':
            in_title_block = True
            continue
        if in_title_block and stripped == ')':
            in_title_block = False
            continue
        if in_title_block and stripped.startswith('(title '):
            indent = line[: len(line) - len(line.lstrip())]
            lines[i] = f'{indent}(title "Powerboard3 - Hierarchy")'
        if in_title_block and stripped.startswith('(date '):
            indent = line[: len(line) - len(line.lstrip())]
            lines[i] = f'{indent}(date "{TODAY}")'


def main():
    original = open(PARENT, 'r', encoding='utf-8').read()
    lines = original.splitlines()

    # Collect top-level sheet blocks
    sheet_ranges = []
    i = 0
    while i < len(lines):
        if lines[i].strip() == '(sheet':
            j = block_end(lines, i)
            sheet_ranges.append((i, j))
            i = j + 1
        else:
            i += 1

    if not sheet_ranges:
        print('No top-level sheets found; nothing to do.')
        return

    sheet_blocks = []
    for s, e in sheet_ranges:
        block = lines[s:e + 1]
        text = '\n'.join(block)
        page_num, page_raw = parse_page_num(text)
        sheet_blocks.append((page_num, page_raw, block))

    # Remove old blocks
    for s, e in reversed(sheet_ranges):
        del lines[s:e + 1]

    # Sort by page number for natural navigation
    sheet_blocks.sort(key=lambda x: (x[0], x[1]))

    # Compute new positioned blocks
    new_blocks = []
    for idx, (_, _, block) in enumerate(sheet_blocks):
        row = idx // COLS
        col = idx % COLS
        x = X0 + col * STEP_X
        y = Y0 + row * STEP_Y
        new_blocks.extend(update_sheet_block(block, x, y))

    # Insert before final closing ')' of schematic
    insert_at = len(lines) - 1
    lines[insert_at:insert_at] = new_blocks

    # Update header metadata
    update_title_and_paper(lines, total_sheets=len(sheet_blocks))

    updated = '\n'.join(lines)
    if original.endswith('\n'):
        updated += '\n'

    if updated != original:
        with open(PARENT, 'w', encoding='utf-8') as f:
            f.write(updated)
        print(f'Organized {len(sheet_blocks)} sheets into {COLS} columns in parent schematic.')
    else:
        print('No changes required.')


if __name__ == '__main__':
    main()
