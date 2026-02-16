#!/usr/bin/env python3
"""Replace ALL remaining EasyEDA power symbols with KiCad native power symbols.
Handles custom power rails by using generic KiCad power symbols with the correct Value."""

import re
import os
import glob

PROJ_DIR = "/Users/nils/Downloads/tryingkicadimport"

# Map EasyEDA power type -> KiCad base symbol to use
# The Value property determines the net name in KiCad
EASYEDA_TO_KICAD_BASE = {
    "5v rail sm-easyedapro:Power-5V": "power:+5V",      # arrow-up style
    "5v rail sm-easyedapro:Power-VCC": "power:VCC",      # arrow-up style
    "5v rail sm-easyedapro:Ground-GND": "power:GND",     # ground triangle
    "5v rail sm-easyedapro:Ground-AGND": "power:GNDA",   # analog ground
}

# KiCad native power symbol templates for lib_symbols section
GND_TEMPLATE = '''		(symbol "power:{name}"
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
			(symbol "{name_esc}_0_1"
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
			(symbol "{name_esc}_1_1"
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
		)'''

VCC_TEMPLATE = '''		(symbol "power:{name}"
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
			(symbol "{name_esc}_0_1"
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
			(symbol "{name_esc}_1_1"
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


def make_lib_symbol(value, is_ground=False):
    """Generate a KiCad power symbol definition for embedding in lib_symbols."""
    template = GND_TEMPLATE if is_ground else VCC_TEMPLATE
    name_esc = value  # KiCad uses the value directly in symbol names
    return template.format(name=value, name_esc=name_esc)


def process_schematic(filepath):
    """Process a single schematic file to replace remaining EasyEDA power symbols."""
    with open(filepath, 'r') as f:
        content = f.read()

    lines = content.split('\n')
    basename = os.path.basename(filepath)

    replacements_made = 0
    needed_lib_symbols = {}  # name -> (definition, is_ground)

    # Find and replace power symbol instances
    i = 0
    while i < len(lines):
        line = lines[i]
        # Look for symbol instance with EasyEDA power lib_id
        if i + 1 < len(lines) and line.strip() == '(symbol':
            lib_match = re.search(r'lib_id "(5v rail sm-easyedapro:(Power-5V|Power-VCC|Ground-GND|Ground-AGND))"', lines[i + 1])
            if lib_match:
                easyeda_lib_id = lib_match.group(1)
                easyeda_type = lib_match.group(2)

                # Find the Value property for this instance
                value = None
                j = i + 2
                depth = 1  # track nesting
                while j < len(lines) and depth > 0:
                    val_match = re.search(r'property "Value" "([^"]*)"', lines[j])
                    if val_match:
                        value = val_match.group(1)
                        break
                    if lines[j].strip().startswith('(symbol'):
                        depth += 1
                    if lines[j].strip() == ')' or lines[j].strip().startswith(')'):
                        pass  # simplified depth tracking
                    j += 1

                if value:
                    is_ground = easyeda_type.startswith("Ground-")

                    # Determine the KiCad lib_id to use
                    # For standard ones that already exist in power lib, use those
                    standard_map = {
                        "GND": "power:GND",
                        "VSS": "power:VSS",
                        "GNDA": "power:GNDA",
                        "AGND": "power:GNDA",
                        "+3V3": "power:+3V3",
                        "+5V": "power:+5V",
                        "+12V": "power:+12V",
                        "VCC": "power:VCC",
                    }

                    if value in standard_map:
                        new_lib_id = standard_map[value]
                        kicad_sym_name = value if value != "AGND" else "GNDA"
                    else:
                        # Custom rail - create a power symbol with this value name
                        new_lib_id = f"power:{value}"
                        kicad_sym_name = value
                        needed_lib_symbols[value] = is_ground

                    # Replace the lib_id
                    lines[i + 1] = lines[i + 1].replace(
                        f'"{easyeda_lib_id}"',
                        f'"{new_lib_id}"'
                    )
                    replacements_made += 1
        i += 1

    if replacements_made == 0:
        return 0

    content = '\n'.join(lines)

    # Add lib_symbol definitions for custom power symbols
    for value, is_ground in needed_lib_symbols.items():
        sym_id = f"power:{value}"
        if f'(symbol "{sym_id}"' not in content:
            lib_sym_def = make_lib_symbol(value, is_ground)
            lib_sym_match = re.search(r'(\(lib_symbols\n)', content)
            if lib_sym_match:
                insert_pos = lib_sym_match.end()
                content = content[:insert_pos] + lib_sym_def + '\n' + content[insert_pos:]

    with open(filepath, 'w') as f:
        f.write(content)

    print(f"  {basename}: {replacements_made} power symbols replaced")
    return replacements_made


def main():
    print("=== Replacing ALL remaining EasyEDA power symbols with KiCad native ===\n")

    total = 0
    for sch_file in sorted(glob.glob(os.path.join(PROJ_DIR, "*.kicad_sch"))):
        if "_autosave" in sch_file:
            continue
        count = process_schematic(sch_file)
        total += count

    print(f"\nTotal: {total} remaining power symbol instances replaced")

    # Verify none left
    remaining = 0
    for sch_file in glob.glob(os.path.join(PROJ_DIR, "*.kicad_sch")):
        if "_autosave" in sch_file:
            continue
        with open(sch_file) as f:
            content = f.read()
        count = len(re.findall(r'lib_id "5v rail sm-easyedapro:(Power-|Ground-)', content))
        remaining += count

    if remaining == 0:
        print("\nAll EasyEDA power symbols have been replaced!")
    else:
        print(f"\nWARNING: {remaining} EasyEDA power symbols still remain")


if __name__ == "__main__":
    main()
