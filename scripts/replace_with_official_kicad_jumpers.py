#!/usr/bin/env python3
import glob
import os

ROOT = "/Users/nils/Downloads/tryingkicadimport"
LIB_PATH = (
    "/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols/Jumper.kicad_sym"
)
TARGETS = {
    "Jumper:SolderJumper_2_Open": "SolderJumper_2_Open",
    "Jumper:SolderJumper_2_Bridged": "SolderJumper_2_Bridged",
}


def extract_symbol_blocks_from_lib(lib_text):
    lines = lib_text.splitlines()
    blocks = {}
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('(symbol "'):
            name = line[len('(symbol "') :].split('"', 1)[0]
            depth = 0
            j = i
            while j < len(lines):
                depth += lines[j].count("(") - lines[j].count(")")
                if depth == 0:
                    break
                j += 1
            if j < len(lines):
                blocks[name] = lines[i : j + 1]
            i = j + 1
        else:
            i += 1
    return blocks


def split_top_level_symbols(sch_lines):
    i = 0
    parts = []
    while i < len(sch_lines):
        if sch_lines[i].strip().startswith('(symbol "'):
            start = i
            depth = 0
            j = i
            while j < len(sch_lines):
                depth += sch_lines[j].count("(") - sch_lines[j].count(")")
                if depth == 0:
                    break
                j += 1
            if j < len(sch_lines):
                parts.append((start, j))
                i = j + 1
                continue
        i += 1
    return parts


def find_lib_symbols_bounds(lines):
    start = None
    for idx, line in enumerate(lines):
        if line.strip() == "(lib_symbols":
            start = idx
            break
    if start is None:
        return None, None

    depth = 0
    j = start
    while j < len(lines):
        depth += lines[j].count("(") - lines[j].count(")")
        if depth == 0:
            return start, j
        j += 1
    return None, None


def replace_targets_in_schematic(path, lib_blocks):
    original = open(path, "r", encoding="utf-8").read()
    original = original.replace(
        '(lib_id "Jumper:SolderJumper_2_Closed")',
        '(lib_id "Jumper:SolderJumper_2_Bridged")',
    )
    original = original.replace(
        '(property "Footprint" "Jumper:SolderJumper-2_Closed"',
        '(property "Footprint" "Jumper:SolderJumper-2_Bridged"',
    )
    original = original.replace(
        '(symbol "Jumper:SolderJumper_2_Closed"',
        '(symbol "Jumper:SolderJumper_2_Bridged"',
    )
    original = original.replace(
        '(symbol "SolderJumper_2_Closed_', '(symbol "SolderJumper_2_Bridged_'
    )
    lines = original.splitlines()

    lib_start, lib_end = find_lib_symbols_bounds(lines)
    if lib_start is None:
        return 0

    lib_lines = lines[lib_start : lib_end + 1]

    symbol_ranges = split_top_level_symbols(lib_lines)
    to_remove = []
    present = set()
    for s, e in symbol_ranges:
        first = lib_lines[s].strip()
        if first.startswith('(symbol "'):
            name = first[len('(symbol "') :].split('"', 1)[0]
            if name in TARGETS:
                to_remove.append((s, e))
                present.add(name)

    # remove existing target symbol blocks (from bottom to top)
    for s, e in reversed(to_remove):
        del lib_lines[s : e + 1]

    # insert official blocks before closing ')' of lib_symbols
    insert_at = len(lib_lines) - 1
    inserted = 0
    for target_name, source_name in sorted(TARGETS.items()):
        if source_name not in lib_blocks:
            continue
        source_block = lib_blocks[source_name]
        first = source_block[0]
        first = first.replace(f'(symbol "{source_name}"', f'(symbol "{target_name}"', 1)
        block = ["\t\t" + first] + ["\t\t" + l for l in source_block[1:]]
        lib_lines[insert_at:insert_at] = block
        insert_at += len(block)
        inserted += 1

    new_lines = lines[:lib_start] + lib_lines + lines[lib_end + 1 :]
    updated = "\n".join(new_lines) + ("\n" if original.endswith("\n") else "")

    if updated != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(updated)
        return inserted
    return 0


def main():
    lib_text = open(LIB_PATH, "r", encoding="utf-8").read()
    lib_blocks = extract_symbol_blocks_from_lib(lib_text)

    missing = {src for src in TARGETS.values() if src not in lib_blocks}
    if missing:
        raise RuntimeError(
            f"Could not find symbols in KiCad library: {sorted(missing)}"
        )

    changed = 0
    files = 0
    for sch in sorted(glob.glob(os.path.join(ROOT, "*.kicad_sch"))):
        inserted = replace_targets_in_schematic(sch, lib_blocks)
        if inserted:
            files += 1
            changed += inserted
            print(
                f"{os.path.basename(sch)}: replaced embedded jumper symbol definitions"
            )

    print(f"\nFiles updated: {files}")
    print(f"Symbol definitions replaced: {changed}")


if __name__ == "__main__":
    main()
