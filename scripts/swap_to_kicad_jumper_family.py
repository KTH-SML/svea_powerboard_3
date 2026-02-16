#!/usr/bin/env python3
import glob
import os
import re

ROOT = "/Users/nils/Downloads/tryingkicadimport"
LIB_PATH = (
    "/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols/Jumper.kicad_sym"
)

INSTANCE_REMAP = {
    "Jumper:SolderJumper_2_Open": "Jumper:Jumper_2_Open",
    "Jumper:SolderJumper_2_Bridged": "Jumper:Jumper_2_Bridged",
}

TARGET_SYMBOLS = {
    "Jumper:Jumper_2_Open": "Jumper_2_Open",
    "Jumper:Jumper_2_Bridged": "Jumper_2_Bridged",
}


def extract_blocks(lib_text):
    lines = lib_text.splitlines()
    blocks = {}
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if s.startswith('(symbol "'):
            name = s[len('(symbol "') :].split('"', 1)[0]
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
                continue
        i += 1
    return blocks


def find_lib_symbols_bounds(lines):
    start = None
    for i, line in enumerate(lines):
        if line.strip() == "(lib_symbols":
            start = i
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


def split_top_symbols(lib_lines):
    out = []
    i = 0
    while i < len(lib_lines):
        if lib_lines[i].strip().startswith('(symbol "'):
            s = i
            d = 0
            j = i
            while j < len(lib_lines):
                d += lib_lines[j].count("(") - lib_lines[j].count(")")
                if d == 0:
                    break
                j += 1
            if j < len(lib_lines):
                out.append((s, j))
                i = j + 1
                continue
        i += 1
    return out


def rewrite_instances(text):
    for old, new in INSTANCE_REMAP.items():
        text = text.replace(f'(lib_id "{old}")', f'(lib_id "{new}")')
    return text


def replace_embedded_defs(text, lib_blocks):
    lines = text.splitlines()
    lib_start, lib_end = find_lib_symbols_bounds(lines)
    if lib_start is None:
        return text, 0

    lib_lines = lines[lib_start : lib_end + 1]

    remove_names = set(INSTANCE_REMAP.keys()) | set(TARGET_SYMBOLS.keys())
    ranges = split_top_symbols(lib_lines)
    to_remove = []
    for s, e in ranges:
        name = lib_lines[s].strip()[len('(symbol "') :].split('"', 1)[0]
        if name in remove_names:
            to_remove.append((s, e))

    for s, e in reversed(to_remove):
        del lib_lines[s : e + 1]

    insert_at = len(lib_lines) - 1  # before closing ) of lib_symbols
    inserted = 0
    for target_name, source_name in TARGET_SYMBOLS.items():
        if source_name not in lib_blocks:
            continue
        src = lib_blocks[source_name]
        first = src[0].replace(
            f'(symbol "{source_name}"', f'(symbol "{target_name}"', 1
        )
        block = ["\t\t" + first] + ["\t\t" + l for l in src[1:]]
        lib_lines[insert_at:insert_at] = block
        insert_at += len(block)
        inserted += 1

    new_lines = lines[:lib_start] + lib_lines + lines[lib_end + 1 :]
    new_text = "\n".join(new_lines)
    if text.endswith("\n"):
        new_text += "\n"
    return new_text, inserted


def process_file(path, lib_blocks):
    original = open(path, "r", encoding="utf-8").read()
    text = rewrite_instances(original)
    text, inserted = replace_embedded_defs(text, lib_blocks)

    if text != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return inserted
    return 0


def main():
    lib_text = open(LIB_PATH, "r", encoding="utf-8").read()
    lib_blocks = extract_blocks(lib_text)

    required = set(TARGET_SYMBOLS.values())
    missing = [name for name in required if name not in lib_blocks]
    if missing:
        raise RuntimeError(f"Missing required KiCad library symbols: {missing}")

    files = sorted(glob.glob(os.path.join(ROOT, "*.kicad_sch")))
    updated_files = 0
    total_defs = 0

    for p in files:
        count = process_file(p, lib_blocks)
        if count:
            updated_files += 1
            total_defs += count
            print(f"{os.path.basename(p)}: swapped to Jumper_2 family")

    print(f"\nFiles updated: {updated_files}")
    print(f"Embedded symbol defs replaced: {total_defs}")


if __name__ == "__main__":
    main()
