#!/usr/bin/env python3
"""Clear power symbol footprints and show power rail values in all schematics."""

import glob
import os
import re

PROJ_DIR = "/Users/nils/Downloads/tryingkicadimport"

EASYEDA_POWER_LIB_RE = re.compile(
    r"5v rail sm-easyedapro:(Power-5V|Power-VCC|Ground-GND|Ground-AGND)"
)


def iter_symbol_blocks(lines):
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped == "(symbol" or stripped.startswith('(symbol "'):
            start = i
            depth = 0
            j = i
            while j < len(lines):
                depth += lines[j].count("(") - lines[j].count(")")
                if depth == 0:
                    break
                j += 1
            if j < len(lines):
                yield start, j
                i = j + 1
                continue
        i += 1


def is_power_symbol_block(block_text):
    if 'property "Reference" "#PWR' in block_text:
        return True
    if 'lib_id "power:' in block_text or '(symbol "power:' in block_text:
        return True
    if EASYEDA_POWER_LIB_RE.search(block_text):
        return True
    return False


def find_block_end(lines, start):
    depth = 0
    i = start
    while i < len(lines):
        depth += lines[i].count("(") - lines[i].count(")")
        if depth == 0:
            return i
        i += 1
    return len(lines) - 1


def process_schematic(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.read().split("\n")

    basename = os.path.basename(filepath)
    footprint_cleared = 0
    value_unhidden = 0

    for start, end in iter_symbol_blocks(lines):
        block_text = "\n".join(lines[start : end + 1])
        if not is_power_symbol_block(block_text):
            continue

        i = start
        while i <= end and i < len(lines):
            line = lines[i]

            if '(property "Footprint" ' in line:
                updated = re.sub(r'(\(property "Footprint" )"[^"]*"', r'\1""', line)
                if updated != line:
                    lines[i] = updated
                    footprint_cleared += 1

            if '(property "Value" ' in line:
                prop_end = find_block_end(lines, i)
                j = i + 1
                while j <= prop_end and j < len(lines):
                    if "(hide yes)" in lines[j]:
                        cleaned = lines[j].replace("(hide yes)", "").rstrip()
                        lines[j] = cleaned
                        value_unhidden += 1
                    j += 1

            i += 1

    updated_content = "\n".join(lines)

    with open(filepath, "r", encoding="utf-8") as f:
        original = f.read()

    if updated_content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(
            f"  {basename}: {footprint_cleared} footprints cleared, {value_unhidden} value hides removed"
        )
        return footprint_cleared + value_unhidden

    return 0


def main():
    print("=== Cleaning power symbols (footprint + value visibility) ===\n")

    total = 0
    for sch_file in sorted(glob.glob(os.path.join(PROJ_DIR, "*.kicad_sch"))):
        if "_autosave" in sch_file:
            continue
        total += process_schematic(sch_file)

    print(f"\nTotal changes applied: {total}")


if __name__ == "__main__":
    main()
