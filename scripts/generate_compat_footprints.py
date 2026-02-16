from pathlib import Path
import re

proj = Path('/Users/nils/Library/CloudStorage/OneDrive-KTH/Work/ITRL/svea_powerboard_rev3/hardware/kicad')
sys_base = Path('/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints')
compat_base = proj / 'libraries' / 'footprints' / 'compat'

maps = {
    'Diode_SMD': {
        'SMA': 'D_SMA',
        'SMB': 'D_SMB',
        'SOD-123': 'D_SOD-123',
        'SOD-123F': 'D_SOD-123F',
        'SOD-123FL': 'D_SOD-123F',
        'SOD-128': 'D_SOD-128',
        'SOD-323': 'D_SOD-323',
    },
    'Package_SO': {
        'MSOP-10_3x3mm_P0.5mm': 'MSOP-10_3x3mm_P0.5mm',
        'SOIC-8_3.9x4.9mm_P1.27mm': 'SOIC-8_3.9x4.9mm_P1.27mm',
        'TSSOP-16_4.4x5mm_P0.65mm': 'TSSOP-16_4.4x5mm_P0.65mm',
        'TSSOP-28_4.4x9.7mm_P0.65mm': 'TSSOP-28_4.4x9.7mm_P0.65mm',
        'VSSOP-10_3.0x3.0mm_P0.5mm': 'VSSOP-10_3x3mm_P0.5mm',
        'VSSOP-8_3.0x3.0mm_P0.65mm': 'VSSOP-8_3x3mm_P0.65mm',
    },
    'Package_DFN_QFN': {
        'QFN-16-1EP_3x3mm_P0.5mm_EP1.7x1.7mm': 'QFN-16-1EP_3x3mm_P0.5mm_EP1.7x1.7mm',
        'QFN-16-1EP_4x4mm_P0.65mm_EP2.2x2.2mm': 'QFN-16-1EP_4x4mm_P0.65mm_EP2.1x2.1mm',
    },
    'Package_LGA': {
        'LGA-14_3x2.5mm_P0.5mm': 'LGA-14_3x2.5mm_P0.5mm_LayoutBorder3x4y',
    },
    'Package_TO_SOT_SMD': {
        'SOT-23': 'SOT-23',
        'SOT-23-5': 'SOT-23-5',
        'SOT-23-6': 'SOT-23-6',
        'SOT-353_SC-70-5': 'SOT-353_SC-70-5',
        'TO-252-2': 'TO-252-2',
        'TO-263-2_TabPin2': 'TO-263-2',
        'TSOT-23-5': 'TSOT-23-5',
        'TSOT-23-6': 'TSOT-23-6',
        'SOT-223-3_TabPin4': 'SOT-223-3_TabPin2',
    }
}

compat_base.mkdir(parents=True, exist_ok=True)
created = []

for lib, mapping in maps.items():
    lib_dir = compat_base / f'{lib}.pretty'
    lib_dir.mkdir(parents=True, exist_ok=True)

    for legacy_name, source_name in mapping.items():
        src = sys_base / f'{lib}.pretty' / f'{source_name}.kicad_mod'
        if not src.exists():
            raise FileNotFoundError(f'Missing source footprint: {src}')

        dst = lib_dir / f'{legacy_name}.kicad_mod'
        text = src.read_text(errors='ignore')
        lines = text.splitlines()
        if lines:
            first = lines[0]
            first = re.sub(r'^\(module\s+[^\s\)]+', f'(module {legacy_name}', first)
            first = re.sub(r'^\(footprint\s+"[^"]+"', f'(footprint "{legacy_name}"', first)
            lines[0] = first
        text = '\n'.join(lines)
        if src.read_text(errors='ignore').endswith('\n'):
            text += '\n'

        dst.write_text(text)
        created.append(dst)

print(f'Created {len(created)} compatibility footprints:')
for p in created:
    print('-', p.relative_to(proj))
