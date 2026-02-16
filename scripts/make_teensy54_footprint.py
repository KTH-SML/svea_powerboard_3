from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
src = ROOT / "5v rail smart enable.pretty" / "Teensy41.kicad_mod"
dst = ROOT / "5v rail smart enable.pretty" / "Teensy40_54.kicad_mod"

text = src.read_text(encoding="utf-8")

# Rename footprint name
text = text.replace('(footprint "Teensy41"', '(footprint "Teensy40_54"', 1)

# Remove pads 55..67 blocks
pad_nums = {str(n) for n in range(55, 68)}


def remove_pad_blocks(data: str) -> str:
    out = []
    i = 0
    while True:
        m = data.find('(pad "', i)
        if m == -1:
            out.append(data[i:])
            break

        out.append(data[i:m])

        num_start = m + len('(pad "')
        num_end = data.find('"', num_start)
        if num_end == -1:
            out.append(data[m:])
            break

        pad_num = data[num_start:num_end]

        # Find full pad s-expression extent
        depth = 0
        j = m
        in_str = False
        esc = False
        while j < len(data):
            c = data[j]
            if in_str:
                if esc:
                    esc = False
                elif c == '\\':
                    esc = True
                elif c == '"':
                    in_str = False
            else:
                if c == '"':
                    in_str = True
                elif c == '(':
                    depth += 1
                elif c == ')':
                    depth -= 1
                    if depth == 0:
                        j += 1
                        break
            j += 1

        block = data[m:j]
        if pad_num not in pad_nums:
            out.append(block)

        i = j

    return ''.join(out)

text = remove_pad_blocks(text)

dst.write_text(text, encoding="utf-8")
print(f"Wrote {dst.name}")
