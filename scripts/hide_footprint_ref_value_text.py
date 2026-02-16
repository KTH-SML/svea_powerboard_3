from pathlib import Path

ROOT = Path(__file__).resolve().parent


def iter_blocks(text: str, start_token: str):
    i = 0
    while True:
        s = text.find(start_token, i)
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


def normalize_property_block(block: str):
    changed = False

    if '(layer "F.SilkS")' in block:
        block = block.replace('(layer "F.SilkS")', '(layer "F.Fab")', 1)
        changed = True
    elif '(layer F.SilkS)' in block:
        block = block.replace('(layer F.SilkS)', '(layer F.Fab)', 1)
        changed = True

    if '(hide yes)' not in block and '(layer "F.Fab")' in block:
        lines = block.splitlines()
        out = []
        inserted = False
        for line in lines:
            out.append(line)
            if not inserted and '(layer "F.Fab")' in line:
                indent = line[: len(line) - len(line.lstrip())]
                out.append(f'{indent}(hide yes)')
                inserted = True
        if inserted:
            block = '\n'.join(out)
            changed = True

    return block, changed


def normalize_old_fp_text_block(block: str):
    changed = False
    if '(layer F.SilkS)' in block:
        block = block.replace('(layer F.SilkS)', '(layer F.Fab)', 1)
        changed = True
    if '(layer "F.SilkS")' in block:
        block = block.replace('(layer "F.SilkS")', '(layer "F.Fab")', 1)
        changed = True
    return block, changed


def process_file(path: Path):
    text = path.read_text(encoding='utf-8')
    original = text

    for token in ['(property "Reference"', '(property "Value"']:
        rebuilt = []
        cursor = 0
        for s, e, block in iter_blocks(text, token):
            rebuilt.append(text[cursor:s])
            new_block, _ = normalize_property_block(block)
            rebuilt.append(new_block)
            cursor = e
        rebuilt.append(text[cursor:])
        text = ''.join(rebuilt)

    for token in ['(fp_text reference', '(fp_text value']:
        rebuilt = []
        cursor = 0
        for s, e, block in iter_blocks(text, token):
            rebuilt.append(text[cursor:s])
            new_block, _ = normalize_old_fp_text_block(block)
            rebuilt.append(new_block)
            cursor = e
        rebuilt.append(text[cursor:])
        text = ''.join(rebuilt)

    if text != original:
        path.write_text(text, encoding='utf-8')
        return True
    return False


changed = 0
for mod in sorted(ROOT.glob('**/*.kicad_mod')):
    if process_file(mod):
        changed += 1

pcb = ROOT / '5v rail smart enable.kicad_pcb'
if pcb.exists() and process_file(pcb):
    changed += 1

print(f'Updated files: {changed}')
