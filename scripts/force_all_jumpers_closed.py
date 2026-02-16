#!/usr/bin/env python3
import glob
import os
import re

ROOT = "/Users/nils/Downloads/tryingkicadimport"


def process_file(path):
    original = open(path, "r", encoding="utf-8").read()
    lines = original.splitlines()

    i = 0
    changed_blocks = 0
    while i < len(lines):
        if lines[i].strip() != "(symbol":
            i += 1
            continue

        start = i
        depth = 0
        j = i
        while j < len(lines):
            depth += lines[j].count("(") - lines[j].count(")")
            if depth == 0:
                break
            j += 1
        if j >= len(lines):
            break

        block = "\n".join(lines[start : j + 1])
        if '(lib_id "Jumper:SolderJumper_2_Open")' in block:
            new_block = block.replace(
                '(lib_id "Jumper:SolderJumper_2_Open")',
                '(lib_id "Jumper:SolderJumper_2_Bridged")',
            )
            new_block = new_block.replace(
                '(property "Footprint" "Jumper:SolderJumper-2_Open"',
                '(property "Footprint" "Jumper:SolderJumper-2_Bridged"',
            )
            if new_block != block:
                lines[start : j + 1] = new_block.split("\n")
                changed_blocks += 1

        i = j + 1

    updated = "\n".join(lines)
    if original.endswith("\n"):
        updated += "\n"

    if updated != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(updated)

    return changed_blocks


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "*.kicad_sch")))
    total = 0
    changed_files = 0

    for path in files:
        count = process_file(path)
        if count:
            changed_files += 1
            total += count
            print(
                f"{os.path.basename(path)}: {count} jumper instance(s) set to Bridged"
            )

    print(f"\nFiles changed: {changed_files}")
    print(f"Total jumper instances set to Bridged: {total}")


if __name__ == "__main__":
    main()
