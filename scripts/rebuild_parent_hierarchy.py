#!/usr/bin/env python3
import math
import re
from datetime import date

PARENT = "/Users/nils/Downloads/tryingkicadimport/5v rail smart enable.kicad_sch"
TODAY = date(2026, 2, 16).isoformat()

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

    seen_property = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('(property '):
            seen_property = True
        if not seen_property and stripped.startswith('(at '):
            lines[i] = set_line_value(line, 'at', [fmt_num(at_x), fmt_num(at_y)])
            break

    for i, line in enumerate(lines):
        if line.strip().startswith('(size '):
            lines[i] = set_line_value(line, 'size', [fmt_num(SHEET_W), fmt_num(SHEET_H)])
            break

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


def main():
    text = open(PARENT, 'r', encoding='utf-8').read()
    lines = text.splitlines()

    uuid_match = re.search(r'\(uuid "([^"]+)"\)', text)
    root_uuid = uuid_match.group(1) if uuid_match else '3f85abf4-0b95-4c4a-b7e9-06f59ca1ea3d'

    # Collect all sheet blocks, even if currently misplaced
    blocks = []
    i = 0
    while i < len(lines):
        if lines[i].strip() == '(sheet':
            j = block_end(lines, i)
            block = lines[i:j + 1]
            page_num, page_raw = parse_page_num('\n'.join(block))
            blocks.append((page_num, page_raw, block))
            i = j + 1
        else:
            i += 1

    if not blocks:
        raise RuntimeError('No sheet blocks found in parent schematic.')

    blocks.sort(key=lambda x: (x[0], x[1]))

    rows = math.ceil(len(blocks) / COLS)
    paper_w = X0 * 2 + (COLS - 1) * STEP_X + SHEET_W
    paper_h = Y0 * 2 + (rows - 1) * STEP_Y + SHEET_H

    out = []
    out.append('(kicad_sch')
    out.append('\t(version 20250114)')
    out.append('\t(generator "eeschema")')
    out.append('\t(generator_version "9.0")')
    out.append(f'\t(uuid "{root_uuid}")')
    out.append(f'\t(paper "User" {fmt_num(paper_w)} {fmt_num(paper_h)})')
    out.append('\t(title_block')
    out.append('\t\t(title "Powerboard3 - Hierarchy")')
    out.append(f'\t\t(date "{TODAY}")')
    out.append('\t\t(company "")')
    out.append('\t)')
    out.append('\t(lib_symbols)')

    for idx, (_, _, block) in enumerate(blocks):
        row = idx // COLS
        col = idx % COLS
        x = X0 + col * STEP_X
        y = Y0 + row * STEP_Y
        updated = update_sheet_block(block, x, y)
        out.extend(updated)

    out.append(')')

    with open(PARENT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out) + '\n')

    print(f'Rebuilt valid parent schematic with {len(blocks)} sheets in {COLS} columns.')


if __name__ == '__main__':
    main()
