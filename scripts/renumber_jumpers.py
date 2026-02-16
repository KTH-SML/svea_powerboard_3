#!/usr/bin/env python3
import glob
import os
import re

ROOT = "/Users/nils/Downloads/tryingkicadimport"
SCH_FILES = sorted(glob.glob(os.path.join(ROOT, "*.kicad_sch")))

JUMPER_LIB_RE = re.compile(r'\(lib_id "Jumper:SolderJumper_2_(Open|Closed)"\)')
PROP_REF_RE = re.compile(r'\(property "Reference" "([^"]+)"')
INST_REF_RE = re.compile(r'\(reference "([^"]+)"\)')
JP_RE = re.compile(r"^JP(\d+)$")


def iter_symbol_blocks(lines):
    i = 0
    while i < len(lines):
        if lines[i].strip() == "(symbol":
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


def collect_used_jp_numbers():
    used = set()
    jp_any_re = re.compile(r'"JP(\d+)"')
    for path in SCH_FILES:
        text = open(path, "r", encoding="utf-8").read()
        for m in jp_any_re.finditer(text):
            used.add(int(m.group(1)))
    return used


def next_free_jp(used):
    n = 1
    while n in used:
        n += 1
    used.add(n)
    return f"JP{n}"


def process_file(path, used_numbers):
    original = open(path, "r", encoding="utf-8").read()
    lines = original.split("\n")

    out = []
    i = 0
    changes = []

    while i < len(lines):
        if lines[i].strip() != "(symbol":
            out.append(lines[i])
            i += 1
            continue

        # parse full top-level symbol block
        start = i
        depth = 0
        j = i
        while j < len(lines):
            depth += lines[j].count("(") - lines[j].count(")")
            if depth == 0:
                break
            j += 1
        if j >= len(lines):
            out.extend(lines[i:])
            break

        block_lines = lines[start : j + 1]
        block_text = "\n".join(block_lines)

        if not JUMPER_LIB_RE.search(block_text):
            out.extend(block_lines)
            i = j + 1
            continue

        prop_ref_match = PROP_REF_RE.search(block_text)
        if not prop_ref_match:
            out.extend(block_lines)
            i = j + 1
            continue

        old_ref = prop_ref_match.group(1)
        new_ref = old_ref

        if not JP_RE.match(old_ref):
            new_ref = next_free_jp(used_numbers)

            block_text = re.sub(
                r'(\(property "Reference" ")' + re.escape(old_ref) + r'(")',
                r"\1" + new_ref + r"\2",
                block_text,
                count=1,
            )
            block_text = re.sub(
                r'(\(reference ")' + re.escape(old_ref) + r'("\))',
                r"\1" + new_ref + r"\2",
                block_text,
            )
            changes.append((old_ref, new_ref))

        out.extend(block_text.split("\n"))
        i = j + 1

    updated = "\n".join(out)
    if updated != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(updated)

    return changes


def main():
    used = collect_used_jp_numbers()
    total = 0
    changed_files = 0

    for path in SCH_FILES:
        changes = process_file(path, used)
        if changes:
            changed_files += 1
            total += len(changes)
            print(f"{os.path.basename(path)}")
            for old_ref, new_ref in changes:
                print(f"  {old_ref} -> {new_ref}")

    print(f"\nChanged files: {changed_files}")
    print(f"Jumper references renamed: {total}")


if __name__ == "__main__":
    main()
