from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
PCB = ROOT / "5v rail smart enable.kicad_pcb"

NUM = r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?"
re_coord = re.compile(rf"\((start|end|center)\s+({NUM})\s+({NUM})\)")
re_pad_at = re.compile(rf"\(pad\s+\"[^\"]+\"[\s\S]*?\(at\s+({NUM})\s+({NUM})(?:\s+{NUM})?\)", re.M)


def iter_blocks(text: str, token: str):
    i = 0
    while True:
        s = text.find(token, i)
        if s == -1:
            break
        depth = 0
        j = s
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
                elif c == '(':
                    depth += 1
                elif c == ')':
                    depth -= 1
                    if depth == 0:
                        j += 1
                        break
            j += 1
        yield s, j, text[s:j]
        i = j


def fmt(v: float) -> str:
    s = f"{v:.2f}".rstrip('0').rstrip('.')
    return s if s else "0"


def extents_from_footprint_block(block: str):
    xs, ys = [], []
    for m in re_coord.finditer(block):
        xs.append(float(m.group(2)))
        ys.append(float(m.group(3)))
    for m in re_pad_at.finditer(block):
        xs.append(float(m.group(1)))
        ys.append(float(m.group(2)))
    if not xs:
        return -1.0, 1.0, -1.0, 1.0
    return min(xs), max(xs), min(ys), max(ys)


def compute_offsets(width: float, height: float):
    span = max(width, height)
    margin = max(0.8, min(2.5, 0.15 * span + 0.8))
    ymax = height / 2.0
    ref_y = ymax + margin
    val_y = ref_y + 1.2
    show_value = span >= 6.0
    return ref_y, val_y, show_value


def build_library_map():
    fmap = {}
    for mod in sorted((ROOT / "5v rail smart enable.pretty").glob("*.kicad_mod")):
        txt = mod.read_text(encoding="utf-8")
        # new format preferred
        if "(footprint \"" in txt:
            for _, _, block in iter_blocks(txt, "(footprint "):
                xmin, xmax, ymin, ymax = extents_from_footprint_block(block)
                ref_y, val_y, show_value = compute_offsets(xmax - xmin, ymax - ymin)
                fmap[mod.stem] = (ref_y, val_y, show_value)
                break
        elif "(module " in txt:
            for _, _, block in iter_blocks(txt, "(module "):
                xmin, xmax, ymin, ymax = extents_from_footprint_block(block)
                ref_y, val_y, show_value = compute_offsets(xmax - xmin, ymax - ymin)
                fmap[mod.stem] = (ref_y, val_y, show_value)
                break
    return fmap


def adjust_property_block(prop_block: str, y: float, layer: str, visible: bool):
    out = re.sub(r"\(at\s+[-+]?\d*\.?\d+\s+[-+]?\d*\.?\d+(?:\s+[-+]?\d*\.?\d+)?\)", f"(at 0 {fmt(y)} 0)", prop_block, count=1)
    out = re.sub(r"\(layer\s+\"[^\"]+\"\)", f"(layer \"{layer}\")", out, count=1)
    if visible:
        out = re.sub(r"\n\s*\(hide\s+yes\)", "", out, count=1)
    else:
        if "(hide yes)" not in out:
            lines = out.splitlines()
            for i, line in enumerate(lines):
                if '(layer "' in line:
                    indent = line[: len(line) - len(line.lstrip())]
                    lines.insert(i + 1, f"{indent}(hide yes)")
                    out = "\n".join(lines)
                    break
    return out


def adjust_footprint_block(block: str, ref_y: float, val_y: float, show_value: bool):
    out = block
    changed = False

    for prop_name, y, layer, vis in [
        ("Reference", ref_y, "F.SilkS", True),
        ("Value", val_y, "F.Fab", show_value),
    ]:
        token = f'(property "{prop_name}"'
        m = out.find(token)
        if m == -1:
            continue
        for s, e, sub in iter_blocks(out[m:], token):
            abs_s = m + s
            abs_e = m + e
            new_sub = adjust_property_block(sub, y, layer, vis)
            if new_sub != sub:
                out = out[:abs_s] + new_sub + out[abs_e:]
                changed = True
            break

    return out, changed


def main():
    fmap = build_library_map()
    text = PCB.read_text(encoding="utf-8")
    rebuilt = []
    cur = 0
    changed_blocks = 0

    for s, e, block in iter_blocks(text, "(footprint "):
        rebuilt.append(text[cur:s])
        cur = e

        m = re.match(r'\(footprint\s+"([^"]+)"', block)
        if not m:
            rebuilt.append(block)
            continue
        full = m.group(1)
        name = full.split(":", 1)[1] if ":" in full else full
        ref_y, val_y, show_value = fmap.get(name, (2.0, 3.2, False))

        new_block, changed = adjust_footprint_block(block, ref_y, val_y, show_value)
        if changed:
            changed_blocks += 1
        rebuilt.append(new_block)

    rebuilt.append(text[cur:])
    new_text = "".join(rebuilt)
    if new_text != text:
        PCB.write_text(new_text, encoding="utf-8")

    print(f"Updated footprints in PCB: {changed_blocks}")


if __name__ == "__main__":
    main()
