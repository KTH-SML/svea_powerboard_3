from pathlib import Path

ROOT = Path(__file__).resolve().parent

MAPPING = {
    '"Jumper:SolderJumper-2_Open"': '"Jumper:SolderJumper-2_P1.3mm_Open_Pad1.0x1.5mm"',
    '"Jumper:SolderJumper-2_Bridged"': '"Jumper:SolderJumper-2_P1.3mm_Bridged_Pad1.0x1.5mm"',
}

updated_files = 0
updated_occurrences = 0

for sch in sorted(ROOT.glob("*.kicad_sch")):
    text = sch.read_text(encoding="utf-8")
    original = text

    for old, new in MAPPING.items():
        count = text.count(old)
        if count:
            text = text.replace(old, new)
            updated_occurrences += count

    if text != original:
        sch.write_text(text, encoding="utf-8")
        updated_files += 1
        print(f"Updated {sch.name}")

print(f"Updated files: {updated_files}")
print(f"Updated occurrences: {updated_occurrences}")
