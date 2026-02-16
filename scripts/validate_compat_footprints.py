from pathlib import Path
import re

root = Path(
    "/Users/nils/Library/CloudStorage/OneDrive-KTH/Work/ITRL/svea_powerboard_rev3/hardware/kicad"
)
fp_table = (root / "fp-lib-table").read_text(errors="ignore")
lib_uri = {
    name: uri
    for name, uri in re.findall(
        r'\(lib \(name "([^"]+)"\)\(type "KiCad"\)\(uri "([^"]+)"\)', fp_table
    )
}

errors = []
for sch in root.rglob("*.kicad_sch"):
    txt = sch.read_text(errors="ignore")
    for fp in re.findall(r'\(property\s+"Footprint"\s+"([^"]+)"', txt):
        if ":" not in fp:
            continue
        lib, name = fp.split(":", 1)
        if lib not in lib_uri:
            continue
        uri = lib_uri[lib].replace("${KIPRJMOD}", str(root))
        if "/compat/" in uri:
            mod = Path(uri) / (name + ".kicad_mod")
            if not mod.exists():
                errors.append(f"{lib}:{name} -> {mod}")

if errors:
    print("MISSING COMPAT FOOTPRINTS:")
    for item in errors:
        print(item)
else:
    print("OK: all footprints that use project compat libs resolve to .kicad_mod files")
