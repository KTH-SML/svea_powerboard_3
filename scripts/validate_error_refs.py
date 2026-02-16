from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
ERROR_REFS = {
    "C206", "U148", "R408", "R394", "R381", "R93", "R92", "R90", "R89", "R88", "R84",
    "R83", "Q70", "Q66", "Q51", "LED2", "LED1", "JP2", "JP1", "D56", "C277", "C276",
    "C255", "C254", "C208", "C207", "U126", "C199", "C198", "C178", "C176", "C90",
    "C82", "C81", "C80", "C78", "21", "12", "11", "5", "R81", "+ESC-CONNECTOR-1", "R476"
}


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

remaining = []
for sch in sorted(ROOT.glob("*.kicad_sch")):
    text = sch.read_text(encoding="utf-8")
    for block in iter_symbol_blocks(text):
        rm = re.search(r'\(property "Reference" "([^"]+)"', block)
        if not rm:
            continue
        ref = rm.group(1)
        if ref in ERROR_REFS and '(property "Footprint" ""' in block and '(on_board yes)' in block:
            remaining.append((sch.name, ref))

if remaining:
    print("REMAINING")
    for row in remaining:
        print(f"{row[0]}: {row[1]}")
else:
    print("OK: none of the listed error refs are on_board yes with empty footprint")
