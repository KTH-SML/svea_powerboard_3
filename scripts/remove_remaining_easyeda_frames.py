#!/usr/bin/env python3
import glob
import os
import re

ROOT = "/Users/nils/Downloads/tryingkicadimport"
DRAWING_LIB_RE = re.compile(r"5v rail sm-easyedapro:Drawing-Symbol_")


def paren_delta_ignoring_quotes(line):
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
            if ch == "(":
                delta += 1
            elif ch == ")":
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


def remove_instances(path):
    original = open(path, "r", encoding="utf-8").read()
    lines = original.splitlines()
    i = 0
    removed = 0

    while i < len(lines):
        if lines[i].strip() == "(symbol":
            j = block_end(lines, i)
            block = "\n".join(lines[i : j + 1])
            m = re.search(r'\(lib_id "([^"]+)"\)', block)
            if m and DRAWING_LIB_RE.search(m.group(1)):
                del lines[i : j + 1]
                removed += 1
                continue
            i = j + 1
        else:
            i += 1

    updated = "\n".join(lines)
    if original.endswith("\n"):
        updated += "\n"

    if updated != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(updated)
    return removed


def main():
    total = 0
    changed = 0
    for p in sorted(glob.glob(os.path.join(ROOT, "*.kicad_sch"))):
        c = remove_instances(p)
        if c:
            changed += 1
            total += c
            print(f"{os.path.basename(p)}: removed {c} Drawing-Symbol instance(s)")
    print(f"\nFiles changed: {changed}")
    print(f"Instances removed: {total}")


if __name__ == "__main__":
    main()
