#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path


FOOTPRINT_MAP = {
    # passives
    '5v rail sm-easyedapro:R0201': 'Resistor_SMD:R_0201_0603Metric',
    '5v rail sm-easyedapro:R0402': 'Resistor_SMD:R_0402_1005Metric',
    '5v rail sm-easyedapro:R0603': 'Resistor_SMD:R_0603_1608Metric',
    '5v rail sm-easyedapro:R0805': 'Resistor_SMD:R_0805_2012Metric',
    '5v rail sm-easyedapro:R1206': 'Resistor_SMD:R_1206_3216Metric',
    '5v rail sm-easyedapro:R1210': 'Resistor_SMD:R_1210_3225Metric',
    '5v rail sm-easyedapro:R2010': 'Resistor_SMD:R_2010_5025Metric',
    '5v rail sm-easyedapro:R2512': 'Resistor_SMD:R_2512_6332Metric',
    '5v rail sm-easyedapro:C0201': 'Capacitor_SMD:C_0201_0603Metric',
    '5v rail sm-easyedapro:C0402': 'Capacitor_SMD:C_0402_1005Metric',
    '5v rail sm-easyedapro:C0603': 'Capacitor_SMD:C_0603_1608Metric',
    '5v rail sm-easyedapro:C0805': 'Capacitor_SMD:C_0805_2012Metric',
    '5v rail sm-easyedapro:C1206': 'Capacitor_SMD:C_1206_3216Metric',
    '5v rail sm-easyedapro:C1210': 'Capacitor_SMD:C_1210_3225Metric',
    '5v rail sm-easyedapro:C2220': 'Capacitor_SMD:C_2220_5750Metric',
    '5v rail sm-easyedapro:L0603': 'Inductor_SMD:L_0603_1608Metric',
    # semiconductors / IC packages
    '5v rail sm-easyedapro:SOT-23-3_L3.0-W1.7-P0.95-LS2.9-BR': 'Package_TO_SOT_SMD:SOT-23',
    '5v rail sm-easyedapro:SOT-23-3_L2.9-W1.3-P1.90-LS2.4-BR': 'Package_TO_SOT_SMD:SOT-23',
    '5v rail sm-easyedapro:SOT-23_L2.9-W1.3-P1.90-LS2.4-BR': 'Package_TO_SOT_SMD:SOT-23',
    '5v rail sm-easyedapro:SOT-23-5_L2.9-W1.6-P0.95-LS2.9-BL': 'Package_TO_SOT_SMD:SOT-23-5',
    '5v rail sm-easyedapro:TSOT-23-5_L2.9-W1.6-P0.95-LS2.8-BL': 'Package_TO_SOT_SMD:TSOT-23-5',
    '5v rail sm-easyedapro:SOT-23-6_L2.9-W1.6-P0.95-LS2.8-BL': 'Package_TO_SOT_SMD:SOT-23-6',
    '5v rail sm-easyedapro:TSOT-23-6_L2.9-W1.6-P0.95-LS2.8-BL': 'Package_TO_SOT_SMD:TSOT-23-6',
    '5v rail sm-easyedapro:SOT-353_L2.1-W1.3-P0.65-LS2.3-BL': 'Package_TO_SOT_SMD:SOT-353_SC-70-5',
    '5v rail sm-easyedapro:SOT-223-3_L6.5-W3.4-P2.30-LS7.0-BR': 'Package_TO_SOT_SMD:SOT-223-3_TabPin2',
    '5v rail sm-easyedapro:TO-252-2_L6.6-W6.1-P4.58-LS9.9-TL': 'Package_TO_SOT_SMD:TO-252-2',
    '5v rail sm-easyedapro:TO-263-2_L10.1-W8.8-P5.08-LS15.4-TL': 'Package_TO_SOT_SMD:TO-263-2_TabPin2',
    '5v rail sm-easyedapro:SOD-123_L2.8-W1.8-LS3.7-RD': 'Diode_SMD:SOD-123',
    '5v rail sm-easyedapro:SOD-123_L2.7-W1.6-LS3.7-RD': 'Diode_SMD:SOD-123',
    '5v rail sm-easyedapro:SOD-123_L2.7-W1.6-LS3.7-FD': 'Diode_SMD:SOD-123',
    '5v rail sm-easyedapro:SOD-123F_L2.8-W1.8-LS3.7-RD': 'Diode_SMD:SOD-123F',
    '5v rail sm-easyedapro:SOD-123FL_L2.8-W1.8-LS3.6-RD': 'Diode_SMD:SOD-123FL',
    '5v rail sm-easyedapro:SOD-128_L3.7-W2.5-LS4.7-RD': 'Diode_SMD:SOD-128',
    '5v rail sm-easyedapro:SOD-323_L1.8-W1.3-LS2.5-RD': 'Diode_SMD:SOD-323',
    '5v rail sm-easyedapro:SMA_L4.4-W2.6-LS5.0-RD': 'Diode_SMD:SMA',
    '5v rail sm-easyedapro:SMA_L4.4-W2.8-LS5.4-RD': 'Diode_SMD:SMA',
    '5v rail sm-easyedapro:SMA_L4.3-W2.6-LS5.0-RD': 'Diode_SMD:SMA',
    '5v rail sm-easyedapro:SMB_L4.6-W3.6-LS5.4-RD': 'Diode_SMD:SMB',
    '5v rail sm-easyedapro:SO-8_L4.9-W3.9-P1.27-LS5.9-BL': 'Package_SO:SOIC-8_3.9x4.9mm_P1.27mm',
    '5v rail sm-easyedapro:MSOP-10_L3.0-W3.0-P0.50-LS5.0-BL': 'Package_SO:MSOP-10_3x3mm_P0.5mm',
    '5v rail sm-easyedapro:TSSOP-16_L5.0-W4.4-P0.65-LS6.4-BL': 'Package_SO:TSSOP-16_4.4x5mm_P0.65mm',
    '5v rail sm-easyedapro:TSSOP-28_L9.7-W4.4-P0.65-LS6.4-TL': 'Package_SO:TSSOP-28_4.4x9.7mm_P0.65mm',
    '5v rail sm-easyedapro:VSSOP-8_L3.0-W3.0-P0.65-LS5.0-BL': 'Package_SO:VSSOP-8_3.0x3.0mm_P0.65mm',
    '5v rail sm-easyedapro:VSSOP-10_L3.0-W3.0-P0.50-LS4.9-BL': 'Package_SO:VSSOP-10_3.0x3.0mm_P0.5mm',
    '5v rail sm-easyedapro:QFN-16_L4.0-W4.0-P0.65-TL-EP2.2': 'Package_DFN_QFN:QFN-16-1EP_4x4mm_P0.65mm_EP2.2x2.2mm',
    '5v rail sm-easyedapro:QFN-16_L3.0-W3.0-P0.50-BL-EP1.7': 'Package_DFN_QFN:QFN-16-1EP_3x3mm_P0.5mm_EP1.7x1.7mm',
    '5v rail sm-easyedapro:TQFN-16_L3.0-W3.0-P0.50-BL-EP1.7': 'Package_DFN_QFN:QFN-16-1EP_3x3mm_P0.5mm_EP1.7x1.7mm',
    '5v rail sm-easyedapro:LGA-14L_L3.0-W2.5-P0.50-TL': 'Package_LGA:LGA-14_3x2.5mm_P0.5mm',
    '5v rail sm-easyedapro:TQFP-48_L7.0-W7.0-P0.50-LS9.0-TL': 'Package_QFP:TQFP-48_7x7mm_P0.5mm',
}

ACRONYM_MAP = {
    'usb': 'USB',
    'esc': 'ESC',
    'bms': 'BMS',
    'imu': 'IMU',
    'pwm': 'PWM',
    'pin': 'PIN',
    'ic': 'IC',
    'jst': 'JST',
    '5v': '5V',
    '12v': '12V',
    '3v3': '3V3',
}


@dataclass
class CleanupStats:
    sheet_blocks: int = 0
    sheet_names_renamed: int = 0
    sheet_layout_changed: bool = False
    remapped_sch_pcb_refs: int = 0
    files_changed: int = 0
    proprietary_refs_before: int = 0
    proprietary_refs_after: int = 0


def fmt_num(value: float) -> str:
    s = f'{value:.4f}'.rstrip('0').rstrip('.')
    return s if s else '0'


def paren_delta_ignoring_quotes(line: str) -> int:
    in_quote = False
    escaped = False
    delta = 0
    for char in line:
        if escaped:
            escaped = False
            continue
        if char == '\\' and in_quote:
            escaped = True
            continue
        if char == '"':
            in_quote = not in_quote
            continue
        if not in_quote:
            if char == '(':
                delta += 1
            elif char == ')':
                delta -= 1
    return delta


def block_end(lines: list[str], start: int) -> int:
    depth = 0
    idx = start
    while idx < len(lines):
        depth += paren_delta_ignoring_quotes(lines[idx])
        if depth == 0:
            return idx
        idx += 1
    return len(lines) - 1


def parse_page_num(sheet_text: str) -> tuple[int, str]:
    match = re.search(r'\(page "([^"]+)"\)', sheet_text)
    if not match:
        return 9999, ''
    raw = match.group(1)
    try:
        return int(raw), raw
    except ValueError:
        return 9999, raw


def set_line_value(line: str, key: str, values: list[str]) -> str:
    indent = line[: len(line) - len(line.lstrip())]
    vals = ' '.join(values)
    return f'{indent}({key} {vals})'


def normalized_sheet_name_from_file(sheet_file: str) -> str:
    base = Path(sheet_file).stem
    base = re.sub(r'^\d+[_\- ]*', '', base)
    raw_tokens = re.split(r'[_\- ]+', base.strip())
    out_tokens: list[str] = []
    for token in raw_tokens:
        if not token:
            continue
        key = token.lower()
        if key in ACRONYM_MAP:
            out_tokens.append(ACRONYM_MAP[key])
        else:
            out_tokens.append(token.capitalize())
    return ' '.join(out_tokens)


def replace_property_value(line: str, property_name: str, new_value: str) -> tuple[str, bool]:
    pattern = rf'(\(property\s+"{re.escape(property_name)}"\s+")([^"]*)(".*)'
    match = re.search(pattern, line)
    if not match:
        return line, False
    if match.group(2) == new_value:
        return line, False
    return f'{match.group(1)}{new_value}{match.group(3)}', True


def update_sheet_block(block_lines: list[str], at_x: float, at_y: float, sheet_w: float, sheet_h: float) -> list[str]:
    lines = block_lines[:]

    seen_property = False
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('(property '):
            seen_property = True
        if not seen_property and stripped.startswith('(at '):
            lines[idx] = set_line_value(line, 'at', [fmt_num(at_x), fmt_num(at_y)])
            break

    for idx, line in enumerate(lines):
        if line.strip().startswith('(size '):
            lines[idx] = set_line_value(line, 'size', [fmt_num(sheet_w), fmt_num(sheet_h)])
            break

    for idx, line in enumerate(lines):
        stripped = line.strip()
        if '(property "Sheetname"' in stripped:
            for probe in range(idx + 1, min(idx + 8, len(lines))):
                if lines[probe].strip().startswith('(at '):
                    lines[probe] = set_line_value(lines[probe], 'at', [fmt_num(at_x), fmt_num(at_y - 0.7116), '0'])
                    break
        if '(property "Sheetfile"' in stripped:
            for probe in range(idx + 1, min(idx + 8, len(lines))):
                if lines[probe].strip().startswith('(at '):
                    lines[probe] = set_line_value(lines[probe], 'at', [fmt_num(at_x), fmt_num(at_y + sheet_h + 0.5846), '0'])
                    break

    return lines


def normalize_parent_hierarchy(parent_schematic: Path, columns: int, x0: float, y0: float, step_x: float, step_y: float, sheet_w: float, sheet_h: float, title: str, stats: CleanupStats) -> None:
    original = parent_schematic.read_text(encoding='utf-8')
    lines = original.splitlines()

    sheet_ranges: list[tuple[int, int]] = []
    idx = 0
    while idx < len(lines):
        if lines[idx].strip() == '(sheet':
            end = block_end(lines, idx)
            sheet_ranges.append((idx, end))
            idx = end + 1
        else:
            idx += 1

    if not sheet_ranges:
        return

    blocks: list[tuple[int, str, list[str]]] = []
    renamed = 0
    for start, end in sheet_ranges:
        block = lines[start : end + 1]

        sheet_file = ''
        for line in block:
            match = re.search(r'\(property\s+"Sheetfile"\s+"([^"]+)"', line)
            if match:
                sheet_file = match.group(1)
                break

        if sheet_file:
            target_name = normalized_sheet_name_from_file(sheet_file)
            for line_index, line in enumerate(block):
                new_line, changed = replace_property_value(line, 'Sheetname', target_name)
                if changed:
                    block[line_index] = new_line
                    renamed += 1
                    break

        page_num, page_raw = parse_page_num('\n'.join(block))
        blocks.append((page_num, page_raw, block))

    stats.sheet_blocks = len(blocks)
    stats.sheet_names_renamed = renamed

    for start, end in reversed(sheet_ranges):
        del lines[start : end + 1]

    blocks.sort(key=lambda item: (item[0], item[1]))

    new_blocks: list[str] = []
    for pos, (_, _, block) in enumerate(blocks):
        row = pos // columns
        col = pos % columns
        at_x = x0 + col * step_x
        at_y = y0 + row * step_y
        new_blocks.extend(update_sheet_block(block, at_x, at_y, sheet_w, sheet_h))

    insert_at = len(lines) - 1
    lines[insert_at:insert_at] = new_blocks

    rows = math.ceil(len(blocks) / columns)
    paper_w = x0 * 2 + (columns - 1) * step_x + sheet_w
    paper_h = y0 * 2 + (rows - 1) * step_y + sheet_h

    in_title_block = False
    for line_index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('(paper '):
            indent = line[: len(line) - len(line.lstrip())]
            lines[line_index] = f'{indent}(paper "User" {fmt_num(paper_w)} {fmt_num(paper_h)})'
        if stripped == '(title_block':
            in_title_block = True
            continue
        if in_title_block and stripped == ')':
            in_title_block = False
            continue
        if in_title_block and stripped.startswith('(title '):
            indent = line[: len(line) - len(line.lstrip())]
            lines[line_index] = f'{indent}(title "{title}")'
        if in_title_block and stripped.startswith('(date '):
            indent = line[: len(line) - len(line.lstrip())]
            lines[line_index] = f'{indent}(date "{date.today().isoformat()}")'

    updated = '\n'.join(lines)
    if original.endswith('\n'):
        updated += '\n'

    if updated != original:
        parent_schematic.write_text(updated, encoding='utf-8')
        stats.files_changed += 1
        stats.sheet_layout_changed = True


def count_proprietary_references(files: list[Path], proprietary_library: str) -> int:
    total = 0
    needle = f'"{proprietary_library}:'
    for file_path in files:
        if not file_path.exists():
            continue
        text = file_path.read_text(encoding='utf-8', errors='ignore')
        total += text.count(needle)
    return total


def remap_footprints(files: list[Path], mapping: dict[str, str], stats: CleanupStats) -> None:
    for file_path in files:
        if not file_path.exists():
            continue
        text = file_path.read_text(encoding='utf-8', errors='ignore')
        original = text
        for old, new in mapping.items():
            matches = text.count(f'"{old}"')
            if matches:
                text = text.replace(f'"{old}"', f'"{new}"')
                stats.remapped_sch_pcb_refs += matches
        if text != original:
            file_path.write_text(text, encoding='utf-8')
            stats.files_changed += 1


def main() -> None:
    parser = argparse.ArgumentParser(description='Normalize KiCad hierarchy naming/layout and remap proprietary footprints to KiCad defaults.')
    parser.add_argument('--kicad-dir', type=Path, default=Path(__file__).resolve().parent.parent / 'hardware' / 'kicad')
    parser.add_argument('--parent', type=str, default='5v rail smart enable.kicad_sch')
    parser.add_argument('--cols', type=int, default=3)
    parser.add_argument('--title', type=str, default='Powerboard3 - Hierarchy')
    parser.add_argument('--proprietary-library', type=str, default='5v rail sm-easyedapro')
    args = parser.parse_args()

    kicad_dir = args.kicad_dir.resolve()
    parent = kicad_dir / args.parent
    if not parent.exists():
        raise FileNotFoundError(f'Parent schematic not found: {parent}')

    schematic_files = sorted(kicad_dir.glob('*.kicad_sch'))
    pcb_file = kicad_dir / '5v rail smart enable.kicad_pcb'
    target_files = schematic_files + ([pcb_file] if pcb_file.exists() else [])

    stats = CleanupStats()
    stats.proprietary_refs_before = count_proprietary_references(target_files, args.proprietary_library)

    normalize_parent_hierarchy(
        parent_schematic=parent,
        columns=args.cols,
        x0=10.0,
        y0=15.0,
        step_x=92.0,
        step_y=26.0,
        sheet_w=82.0,
        sheet_h=18.0,
        title=args.title,
        stats=stats,
    )
    remap_footprints(target_files, FOOTPRINT_MAP, stats)
    stats.proprietary_refs_after = count_proprietary_references(target_files, args.proprietary_library)

    print(f'kicad_dir: {kicad_dir}')
    print(f'sheet_blocks: {stats.sheet_blocks}')
    print(f'sheet_names_renamed: {stats.sheet_names_renamed}')
    print(f'sheet_layout_changed: {stats.sheet_layout_changed}')
    print(f'footprint_remaps: {stats.remapped_sch_pcb_refs}')
    print(f'files_changed: {stats.files_changed}')
    print(f'proprietary_refs_before: {stats.proprietary_refs_before}')
    print(f'proprietary_refs_after: {stats.proprietary_refs_after}')


if __name__ == '__main__':
    main()