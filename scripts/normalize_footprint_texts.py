from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent

kicad_mod_files = sorted(ROOT.glob("**/*.kicad_mod"))

re_prop_ref = re.compile(r'(\(property\s+"Reference"\s+")([^"]*)(")')
re_prop_val = re.compile(r'(\(property\s+"Value"\s+")([^"]*)(")')

re_old_fp_ref = re.compile(r'(\(fp_text\s+reference\s+)([^\s\)\"]+|"[^"]*")')
re_old_fp_val = re.compile(r'(\(fp_text\s+value\s+)([^\s\)\"]+|"[^"]*")')

# convert user text that looks like a specific refdes (R123, U7, JP2, LED1, etc.)
re_fp_user_refdes = re.compile(r'(\(fp_text\s+user\s+")([A-Za-z\+\-]{1,12}[0-9]{1,4})(")')

files_changed = 0
changes = {
    "prop_ref": 0,
    "prop_val": 0,
    "old_ref": 0,
    "old_val": 0,
    "user_refdes": 0,
}

for mod in kicad_mod_files:
    text = mod.read_text(encoding="utf-8")
    original = text

    def sub_prop_ref(m):
        if m.group(2) == "REF**":
            return m.group(0)
        changes["prop_ref"] += 1
        return f'{m.group(1)}REF**{m.group(3)}'

    def sub_prop_val(m):
        if m.group(2) == "${VALUE}":
            return m.group(0)
        changes["prop_val"] += 1
        return f'{m.group(1)}${{VALUE}}{m.group(3)}'

    def sub_old_ref(m):
        token = m.group(2)
        if token == 'REF**' or token == '"REF**"':
            return m.group(0)
        changes["old_ref"] += 1
        return f'{m.group(1)}REF**'

    def sub_old_val(m):
        token = m.group(2)
        if token == '"${VALUE}"' or token == '${VALUE}':
            return m.group(0)
        changes["old_val"] += 1
        return f'{m.group(1)}"${{VALUE}}"'

    def sub_user_refdes(m):
        changes["user_refdes"] += 1
        return f'{m.group(1)}${{REFERENCE}}{m.group(3)}'

    text = re_prop_ref.sub(sub_prop_ref, text)
    text = re_prop_val.sub(sub_prop_val, text)
    text = re_old_fp_ref.sub(sub_old_ref, text)
    text = re_old_fp_val.sub(sub_old_val, text)
    text = re_fp_user_refdes.sub(sub_user_refdes, text)

    if text != original:
        mod.write_text(text, encoding="utf-8")
        files_changed += 1

print(f"Files changed: {files_changed}")
for k, v in changes.items():
    print(f"{k}: {v}")
