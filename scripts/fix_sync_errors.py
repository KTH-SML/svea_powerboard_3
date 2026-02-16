from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent

# From the latest error list shared by user (no-footprint assigned)
NO_FP_REFS = {
    "C206", "U148", "R408", "R394", "R381", "R93", "R92", "R90", "R89", "R88", "R84",
    "R83", "Q70", "Q66", "Q51", "LED2", "LED1", "JP2", "JP1", "D56", "C277", "C276",
    "C255", "C254", "C208", "C207", "U126", "C199", "C198", "C178", "C176", "C90",
    "C82", "C81", "C80", "C78", "21", "12", "11", "5", "R81", "+ESC-CONNECTOR-1", "R476"
}


def iter_symbol_blocks(text: str):
    i = 0
    while True:
        start = text.find("(symbol", i)
        if start == -1:
            break
        depth = 0
        j = start
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
        yield start, j, text[start:j]
        i = j


updated_files = 0
u183_fix_count = 0
no_fp_offboard_count = 0

for sch in sorted(ROOT.glob("*.kicad_sch")):
    text = sch.read_text(encoding="utf-8")
    original = text

    # 1) Fix U183 footprint mismatch (Teensy4.0 symbol has pins up to 54, so use Teensy41 footprint)
    if sch.name == "30_Microcontroller extra.kicad_sch":
        c = text.count('"5v rail sm-easyedapro:Teensy40"')
        if c:
            text = text.replace('"5v rail sm-easyedapro:Teensy40"', '"5v rail sm-easyedapro:Teensy41"')
            u183_fix_count += c

    # 2) Mark listed empty-footprint symbols as not on board / not in BOM
    rebuilt = []
    cursor = 0
    changed_local = 0

    for start, end, block in iter_symbol_blocks(text):
        rebuilt.append(text[cursor:start])
        cursor = end

        rm = re.search(r'\(property "Reference" "([^"]+)"', block)
        ref = rm.group(1) if rm else None

        if (
            ref in NO_FP_REFS
            and '(property "Footprint" ""' in block
            and '(on_board yes)' in block
        ):
            new_block = block.replace('(on_board yes)', '(on_board no)', 1)
            if '(in_bom yes)' in new_block:
                new_block = new_block.replace('(in_bom yes)', '(in_bom no)', 1)
            changed_local += 1
            rebuilt.append(new_block)
        else:
            rebuilt.append(block)

    rebuilt.append(text[cursor:])
    text = ''.join(rebuilt)
    no_fp_offboard_count += changed_local

    if text != original:
        sch.write_text(text, encoding="utf-8")
        updated_files += 1
        print(f"Updated {sch.name}")

print(f"Updated files: {updated_files}")
print(f"U183 footprint replacements: {u183_fix_count}")
print(f"No-footprint symbols set off-board: {no_fp_offboard_count}")
