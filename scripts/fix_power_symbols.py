#!/usr/bin/env python3
"""Replace EasyEDA power symbols with KiCad native power symbols in all schematics."""

import re
import os
import glob

PROJ_DIR = "/Users/nils/Downloads/tryingkicadimport"

# Mapping: (easyeda_lib_id, value) -> kicad_lib_id
# Only replace standard power rails that have native KiCad equivalents
STANDARD_REPLACEMENTS = {
    ("5v rail sm-easyedapro:Ground-GND", "GND"): "power:GND",
    ("5v rail sm-easyedapro:Ground-GND", "VSS"): "power:VSS",
    ("5v rail sm-easyedapro:Ground-AGND", "AGND"): "power:GNDA",
    ("5v rail sm-easyedapro:Power-5V", "+3V3"): "power:+3V3",
    ("5v rail sm-easyedapro:Power-5V", "+5V"): "power:+5V",
    ("5v rail sm-easyedapro:Power-5V", "+12V"): "power:+12V",
    ("5v rail sm-easyedapro:Power-VCC", "VCC"): "power:VCC",
}

# KiCad native power symbol lib_symbols definitions (embedded in schematic)
# These are the standard KiCad 9 power symbol definitions
KICAD_POWER_LIB_SYMBOLS = {
    "power:GND": '''		(symbol "power:GND"
			(power)
			(pin_numbers
				(hide yes)
			)
			(pin_names
				(offset 0)
				(hide yes)
			)
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "#PWR"
				(at 0 -3.81 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Value" "GND"
				(at 0 -3.81 0)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Footprint" ""
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Datasheet" ""
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Description" "Power symbol creates a global label with name \\"GND\\" ; ground"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "ki_keywords" "global power"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(symbol "GND_0_1"
				(polyline
					(pts
						(xy 0 0) (xy 0 -1.27) (xy 1.27 -1.27) (xy 0 -2.54) (xy -1.27 -1.27) (xy 0 -1.27)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
			)
			(symbol "GND_1_1"
				(pin power_in line
					(at 0 0 270)
					(length 0)
					(name "~"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "1"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
			)
			(embedded_fonts no)
		)''',

    "power:VSS": '''		(symbol "power:VSS"
			(power)
			(pin_numbers
				(hide yes)
			)
			(pin_names
				(offset 0)
				(hide yes)
			)
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "#PWR"
				(at 0 -3.81 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Value" "VSS"
				(at 0 -3.81 0)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Footprint" ""
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Datasheet" ""
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Description" "Power symbol creates a global label with name \\"VSS\\" ; ground"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "ki_keywords" "global power"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(symbol "VSS_0_1"
				(polyline
					(pts
						(xy 0 0) (xy 0 -1.27) (xy 1.27 -1.27) (xy 0 -2.54) (xy -1.27 -1.27) (xy 0 -1.27)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
			)
			(symbol "VSS_1_1"
				(pin power_in line
					(at 0 0 270)
					(length 0)
					(name "~"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "1"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
			)
			(embedded_fonts no)
		)''',

    "power:GNDA": '''		(symbol "power:GNDA"
			(power)
			(pin_numbers
				(hide yes)
			)
			(pin_names
				(offset 0)
				(hide yes)
			)
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "#PWR"
				(at 0 -3.81 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Value" "GNDA"
				(at 0 -3.81 0)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Footprint" ""
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Datasheet" ""
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Description" "Power symbol creates a global label with name \\"GNDA\\" ; analog ground"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "ki_keywords" "global power"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(symbol "GNDA_0_1"
				(polyline
					(pts
						(xy 0 0) (xy 0 -1.27) (xy 1.27 -1.27) (xy 0 -2.54) (xy -1.27 -1.27) (xy 0 -1.27)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
			)
			(symbol "GNDA_1_1"
				(pin power_in line
					(at 0 0 270)
					(length 0)
					(name "~"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "1"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
			)
			(embedded_fonts no)
		)''',
}

# Template for positive power symbols (+3V3, +5V, +12V, VCC)
POSITIVE_POWER_TEMPLATE = '''		(symbol "power:{name}"
			(power)
			(pin_numbers
				(hide yes)
			)
			(pin_names
				(offset 0)
				(hide yes)
			)
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "#PWR"
				(at 0 -3.81 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Value" "{name}"
				(at 0 3.81 0)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Footprint" ""
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Datasheet" ""
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Description" "Power symbol creates a global label with name \\"{name}\\""
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "ki_keywords" "global power"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(symbol "{name_safe}_0_1"
				(polyline
					(pts
						(xy -0.762 1.27) (xy 0 2.54)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(polyline
					(pts
						(xy 0 2.54) (xy 0.762 1.27)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(polyline
					(pts
						(xy 0 0) (xy 0 2.54)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
			)
			(symbol "{name_safe}_1_1"
				(pin power_in line
					(at 0 0 90)
					(length 0)
					(name "~"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "1"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
			)
			(embedded_fonts no)
		)'''

# Generate positive power symbols
for name in ["+3V3", "+5V", "+12V", "VCC"]:
    key = f"power:{name}"
    if key not in KICAD_POWER_LIB_SYMBOLS:
        name_safe = name.replace("+", "+")  # keep as-is for KiCad
        KICAD_POWER_LIB_SYMBOLS[key] = POSITIVE_POWER_TEMPLATE.format(
            name=name, name_safe=name
        )


def find_symbol_instances(content):
    """Find all power symbol instances and their lib_id + value."""
    instances = []
    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        # Look for symbol instance start (not in lib_symbols)
        if '\t(symbol' == line[:8] if line.startswith('\t(symbol') else False:
            # Check next line for lib_id
            if i + 1 < len(lines):
                lib_match = re.search(r'lib_id "([^"]*)"', lines[i + 1])
                if lib_match:
                    lib_id = lib_match.group(1)
                    if lib_id.startswith("5v rail sm-easyedapro:Power-") or \
                       lib_id.startswith("5v rail sm-easyedapro:Ground-"):
                        # Find the Value property
                        value = None
                        lib_id_line = i + 1
                        j = i + 2
                        while j < len(lines) and not (lines[j].startswith('\t(symbol') or lines[j].startswith('\t)')):
                            val_match = re.search(r'property "Value" "([^"]*)"', lines[j])
                            if val_match:
                                value = val_match.group(1)
                                break
                            j += 1
                        if value:
                            instances.append({
                                'lib_id': lib_id,
                                'value': value,
                                'lib_id_line_num': lib_id_line,
                            })
        i += 1
    return instances


def process_schematic(filepath):
    """Process a single schematic file."""
    with open(filepath, 'r') as f:
        content = f.read()

    lines = content.split('\n')
    basename = os.path.basename(filepath)

    # Find power symbol instances
    instances = find_symbol_instances(content)
    if not instances:
        return 0

    replacements_made = 0
    needed_lib_symbols = set()

    # Phase 1: Replace lib_id in symbol instances
    for inst in instances:
        key = (inst['lib_id'], inst['value'])
        if key in STANDARD_REPLACEMENTS:
            new_lib_id = STANDARD_REPLACEMENTS[key]
            old_line = lines[inst['lib_id_line_num']]
            new_line = old_line.replace(
                f'"{inst["lib_id"]}"',
                f'"{new_lib_id}"'
            )
            lines[inst['lib_id_line_num']] = new_line
            needed_lib_symbols.add(new_lib_id)
            replacements_made += 1

    if replacements_made == 0:
        return 0

    content = '\n'.join(lines)

    # Phase 2: Add KiCad power lib_symbol definitions to lib_symbols section
    # Find the lib_symbols section
    for lib_sym_id in needed_lib_symbols:
        # Check if already present
        if f'(symbol "{lib_sym_id}"' in content:
            continue
        # Find insertion point: right after (lib_symbols line
        lib_sym_match = re.search(r'(\(lib_symbols\n)', content)
        if lib_sym_match:
            insert_pos = lib_sym_match.end()
            content = content[:insert_pos] + KICAD_POWER_LIB_SYMBOLS[lib_sym_id] + '\n' + content[insert_pos:]

    # Phase 3: Update Value property for GNDA (was AGND, KiCad uses GNDA)
    # The net name in KiCad comes from the power symbol's pin, which for power:GNDA creates net "GNDA"
    # But the user's schematics have Value "AGND". We need to change Value to "GNDA" for power:GNDA
    content = re.sub(
        r'(lib_id "power:GNDA"\).*?property "Value" )"AGND"',
        r'\1"GNDA"',
        content,
        flags=re.DOTALL
    )

    with open(filepath, 'w') as f:
        f.write(content)

    print(f"  {basename}: {replacements_made} power symbols replaced")
    return replacements_made


def main():
    print("=== Replacing EasyEDA power symbols with KiCad native symbols ===\n")
    print("Replacements:")
    for (old_id, val), new_id in sorted(STANDARD_REPLACEMENTS.items()):
        print(f"  {old_id} (Value={val}) -> {new_id}")
    print()

    total = 0
    for sch_file in sorted(glob.glob(os.path.join(PROJ_DIR, "*.kicad_sch"))):
        if "_autosave" in sch_file:
            continue
        count = process_schematic(sch_file)
        total += count

    print(f"\nTotal: {total} power symbol instances replaced across all schematics")
    print("\nCustom power rails left as-is (no native KiCad equivalent):")
    print("  PACK+, PACK-, CHG+, VCC_ESC, +5V-USBC, +SERVO_VCC,")
    print("  IN-CHARGING-VCC, IN-CHARGING-VCC-LIMITED, IN-CHARGING-VCC-USBC,")
    print("  OUT-CHARGING-VCC, VCC-KICKSTART, PB_3V3")


if __name__ == "__main__":
    main()
