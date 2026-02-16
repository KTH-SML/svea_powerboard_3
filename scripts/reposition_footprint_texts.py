from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent

NUM = r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?"
re_point = re.compile(rf"\((start|end|center|at)\s+({NUM})\s+({NUM})(?:\s+{NUM})?\)")


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


def get_extents(block: str):
    xs, ys = [], []
    for m in re_point.finditer(block):
        x = float(m.group(2))
        y = float(m.group(3))
        xs.append(x)
        ys.append(y)
    if not xs:
        return -1.0, 1.0, -1.0, 1.0
    return min(xs), max(xs), min(ys), max(ys)


def adjust_property_block(prop_block: str, name: str, y: float, layer: str, visible: bool):
    out = prop_block

    out = re.sub(r"\(at\s+[-+]?\d*\.?\d+\s+[-+]?\d*\.?\d+(?:\s+[-+]?\d*\.?\d+)?\)", f"(at 0 {fmt(y)} 0)", out, count=1)

    out = re.sub(r"\(layer\s+\"[^\"]+\"\)", f"(layer \"{layer}\")", out, count=1)

    if visible:
        out = re.sub(r"\n\s*\(hide\s+yes\)", "", out, count=1)
    else:
        if "(hide yes)" not in out:
            lines = out.splitlines()
            inserted = False
            for i, line in enumerate(lines):
                if '(layer "' in line:
                    indent = line[: len(line) - len(line.lstrip())]
                    lines.insert(i + 1, f"{indent}(hide yes)")
                    inserted = True
                    break
            if inserted:
                out = "\n".join(lines)

    return out


def update_new_style_footprint(block: str):
    xmin, xmax, ymin, ymax = get_extents(block)
    width = xmax - xmin
    height = ymax - ymin
    span = max(width, height)

    margin = max(0.8, min(2.5, 0.15 * span + 0.8))
    ref_y = ymax + margin
    val_y = ref_y + 1.2

    show_value = span >= 6.0

    changed = False
    out = block

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
            new_sub = adjust_property_block(sub, prop_name, y, layer, vis)
            if new_sub != sub:
                out = out[:abs_s] + new_sub + out[abs_e:]
                changed = True
            break

    return out, changed


def update_old_style_module(block: str):
    xmin, xmax, ymin, ymax = get_extents(block)
    width = xmax - xmin
    height = ymax - ymin
    span = max(width, height)

    margin = max(0.8, min(2.5, 0.15 * span + 0.8))
    ref_y = ymax + margin
    val_y = ref_y + 1.2
    show_value = span >= 6.0

    out = block
    changed = False

    def repl_fp_text(kind: str, y: float, layer: str, visible: bool):
        nonlocal out, changed
        pat = re.compile(rf"\(fp_text\s+{kind}\s+([^\s\)]+|\"[^\"]*\")\s+\(at\s+[^\)]*\)\s+\(layer\s+[^\)]*\)", re.S)
        m = pat.search(out)
        if not m:
            return

        txt = m.group(1)
        if kind == "reference":
            txt = "REF**"
        elif kind == "value":
            txt = '"${VALUE}"'

        new_head = f"(fp_text {kind} {txt} (at 0 {fmt(y)} 0) (layer {layer})"
        old_head = m.group(0)
        if new_head != old_head:
            out = out[:m.start()] + new_head + out[m.end():]
            changed = True

        if visible:
            out2 = re.sub(rf"\(fp_text\s+{kind}[\s\S]*?\n\s*\(hide\s+yes\)", lambda x: x.group(0).replace("\n\t\t(hide yes)", "").replace("\n  (hide yes)", ""), out, count=1)
            if out2 != out:
                out = out2
                changed = True

    repl_fp_text("reference", ref_y, "F.SilkS", True)
    repl_fp_text("value", val_y, "F.Fab", show_value)

    return out, changed


def process_file(path: Path):
    text = path.read_text(encoding="utf-8")
    original = text

    # New-style footprints
    rebuilt = []
    cur = 0
    for s, e, block in iter_blocks(text, "(footprint "):
        rebuilt.append(text[cur:s])
        new_block, _ = update_new_style_footprint(block)
        rebuilt.append(new_block)
        cur = e
    rebuilt.append(text[cur:])
    text = "".join(rebuilt)

    # Old-style modules
    rebuilt = []
    cur = 0
    for s, e, block in iter_blocks(text, "(module "):
        rebuilt.append(text[cur:s])
        new_block, _ = update_old_style_module(block)
        rebuilt.append(new_block)
        cur = e
    rebuilt.append(text[cur:])
    text = "".join(rebuilt)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


changed_files = 0
for mod in sorted(ROOT.glob("**/*.kicad_mod")):
    if process_file(mod):
        changed_files += 1

pcb = ROOT / "5v rail smart enable.kicad_pcb"
if pcb.exists() and process_file(pcb):
    changed_files += 1

print(f"Updated files: {changed_files}")
