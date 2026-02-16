from pathlib import Path

ROOT = Path(__file__).resolve().parent

PASSIVE_MAP = {
    '5v rail sm-easyedapro:R0201': 'Resistor_SMD:R_0201_0603Metric',
    '5v rail sm-easyedapro:R0402': 'Resistor_SMD:R_0402_1005Metric',
    '5v rail sm-easyedapro:R0603': 'Resistor_SMD:R_0603_1608Metric',
    '5v rail sm-easyedapro:R0805': 'Resistor_SMD:R_0805_2012Metric',
    '5v rail sm-easyedapro:R1206': 'Resistor_SMD:R_1206_3216Metric',
    '5v rail sm-easyedapro:R1210': 'Resistor_SMD:R_1210_3225Metric',
    '5v rail sm-easyedapro:R2010': 'Resistor_SMD:R_2010_5025Metric',
    '5v rail sm-easyedapro:R2512': 'Resistor_SMD:R_2512_6332Metric',

    '5v rail sm-easyedapro:C0201': 'Capacitor_SMD:C_0201_0603Metric',
    '5v rail sm-easyedapro:C0402': 'Capacitor_SMD:C_0402_1005Metric',
    '5v rail sm-easyedapro:C0603': 'Capacitor_SMD:C_0603_1608Metric',
    '5v rail sm-easyedapro:C0805': 'Capacitor_SMD:C_0805_2012Metric',
    '5v rail sm-easyedapro:C1206': 'Capacitor_SMD:C_1206_3216Metric',
    '5v rail sm-easyedapro:C1210': 'Capacitor_SMD:C_1210_3225Metric',
    '5v rail sm-easyedapro:C2220': 'Capacitor_SMD:C_2220_5750Metric',

    '5v rail sm-easyedapro:L0603': 'Inductor_SMD:L_0603_1608Metric',
}


REMOVE_USER_TEXTS = {
    '"${REFERENCE}"',
    '"${VALUE}"',
    '"REFERENCE"',
    '"Reference"',
    '"REF"',
}


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


def remove_center_user_texts(text: str):
    rebuilt = []
    cur = 0
    removed = 0

    for s, e, block in iter_blocks(text, '(fp_text user '):
        rebuilt.append(text[cur:s])
        cur = e

        # first line token extraction
        first_line = block.splitlines()[0]
        # examples:
        # (fp_text user "${REFERENCE}"
        # (fp_text user REFERENCE (at ...)
        token = None
        parts = first_line.replace('\t', ' ').split()
        # Typical first line: (fp_text user "${REFERENCE}"
        # Tokens -> ['(fp_text', 'user', '"${REFERENCE}"']
        if len(parts) >= 3:
            token = parts[2]
        if token in REMOVE_USER_TEXTS:
            removed += 1
            continue

        rebuilt.append(block)

    rebuilt.append(text[cur:])
    return ''.join(rebuilt), removed


changes = {
    'schematic_replacements': 0,
    'pcb_replacements': 0,
    'mod_user_text_removed': 0,
    'pcb_user_text_removed': 0,
    'files_changed': 0,
}

# 1) Replace passives in schematics
for sch in sorted(ROOT.glob('*.kicad_sch')):
    text = sch.read_text(encoding='utf-8')
    original = text
    for old, new in PASSIVE_MAP.items():
        count = text.count(f'"{old}"')
        if count:
            text = text.replace(f'"{old}"', f'"{new}"')
            changes['schematic_replacements'] += count
    if text != original:
        sch.write_text(text, encoding='utf-8')
        changes['files_changed'] += 1

# 2) Replace passives + remove user texts in PCB
pcb = ROOT / '5v rail smart enable.kicad_pcb'
if pcb.exists():
    text = pcb.read_text(encoding='utf-8')
    original = text
    for old, new in PASSIVE_MAP.items():
        count = text.count(f'"{old}"')
        if count:
            text = text.replace(f'"{old}"', f'"{new}"')
            changes['pcb_replacements'] += count

    text, removed = remove_center_user_texts(text)
    changes['pcb_user_text_removed'] += removed

    if text != original:
        pcb.write_text(text, encoding='utf-8')
        changes['files_changed'] += 1

# 3) Remove same user texts from footprint libraries
for mod in sorted(ROOT.glob('**/*.kicad_mod')):
    text = mod.read_text(encoding='utf-8')
    original = text
    text, removed = remove_center_user_texts(text)
    changes['mod_user_text_removed'] += removed
    if text != original:
        mod.write_text(text, encoding='utf-8')
        changes['files_changed'] += 1

for k, v in changes.items():
    print(f'{k}: {v}')
