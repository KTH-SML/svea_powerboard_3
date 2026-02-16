from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent


def iter_symbol_blocks(text: str):
    i = 0
    while True:
        m = text.find("(symbol", i)
        if m == -1:
            break
        depth = 0
        j = m
        in_str = False
        esc = False
        while j < len(text):
            c = text[j]
            if in_str:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == '"':
                    in_str = False
            else:
                if c == '"':
                    in_str = True
                elif c == "(":
                    depth += 1
                elif c == ")":
                    depth -= 1
                    if depth == 0:
                        j += 1
                        break
            j += 1
        yield text[m:j]
        i = j


count = 0
rows = []
for sch in sorted(ROOT.glob("*.kicad_sch")):
    text = sch.read_text(encoding="utf-8")
    for block in iter_symbol_blocks(text):
        if '(property "Footprint" ""' in block and '(on_board yes)' in block:
            rm = re.search(r'\(property "Reference" "([^"]+)"', block)
            ref = rm.group(1) if rm else "?"
            if ref.startswith("#"):
                continue
            count += 1
            rows.append((sch.name, ref))

print(f"count={count}")
for sch_name, ref in rows:
    print(f"{sch_name}: {ref}")
