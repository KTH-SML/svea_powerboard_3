from pathlib import Path

ROOT = Path(__file__).resolve().parent

FILES = sorted(ROOT.glob('*.kicad_sch')) + [ROOT / '5v rail smart enable.kicad_pcb']

MAP = {
    '5v rail sm-easyedapro:SOT-23-3_L3.0-W1.7-P0.95-LS2.9-BR': 'Package_TO_SOT_SMD:SOT-23',
    '5v rail sm-easyedapro:SOT-23-3_L2.9-W1.3-P1.90-LS2.4-BR': 'Package_TO_SOT_SMD:SOT-23',
    '5v rail sm-easyedapro:SOT-23_L2.9-W1.3-P1.90-LS2.4-BR': 'Package_TO_SOT_SMD:SOT-23',
    '5v rail sm-easyedapro:SOT-23-5_L2.9-W1.6-P0.95-LS2.9-BL': 'Package_TO_SOT_SMD:SOT-23-5',
    '5v rail sm-easyedapro:TSOT-23-5_L2.9-W1.6-P0.95-LS2.8-BL': 'Package_TO_SOT_SMD:TSOT-23-5',
    '5v rail sm-easyedapro:SOT-23-6_L2.9-W1.6-P0.95-LS2.8-BL': 'Package_TO_SOT_SMD:SOT-23-6',
    '5v rail sm-easyedapro:TSOT-23-6_L2.9-W1.6-P0.95-LS2.8-BL': 'Package_TO_SOT_SMD:TSOT-23-6',
    '5v rail sm-easyedapro:SOT-353_L2.1-W1.3-P0.65-LS2.3-BL': 'Package_TO_SOT_SMD:SOT-353_SC-70-5',
    '5v rail sm-easyedapro:SOT-223-3_L6.5-W3.4-P2.30-LS7.0-BR': 'Package_TO_SOT_SMD:SOT-223-3_TabPin2',
    '5v rail sm-easyedapro:TO-252-2_L6.6-W6.1-P4.58-LS9.9-TL': 'Package_TO_SOT_SMD:TO-252-2',
    '5v rail sm-easyedapro:TO-263-2_L10.1-W8.8-P5.08-LS15.4-TL': 'Package_TO_SOT_SMD:TO-263-2_TabPin2',

    '5v rail sm-easyedapro:SOD-123_L2.8-W1.8-LS3.7-RD': 'Diode_SMD:SOD-123',
    '5v rail sm-easyedapro:SOD-123_L2.7-W1.6-LS3.7-RD': 'Diode_SMD:SOD-123',
    '5v rail sm-easyedapro:SOD-123_L2.7-W1.6-LS3.7-FD': 'Diode_SMD:SOD-123',
    '5v rail sm-easyedapro:SOD-123F_L2.8-W1.8-LS3.7-RD': 'Diode_SMD:SOD-123F',
    '5v rail sm-easyedapro:SOD-123FL_L2.8-W1.8-LS3.6-RD': 'Diode_SMD:SOD-123FL',
    '5v rail sm-easyedapro:SOD-128_L3.7-W2.5-LS4.7-RD': 'Diode_SMD:SOD-128',
    '5v rail sm-easyedapro:SOD-323_L1.8-W1.3-LS2.5-RD': 'Diode_SMD:SOD-323',
    '5v rail sm-easyedapro:SMA_L4.4-W2.6-LS5.0-RD': 'Diode_SMD:SMA',
    '5v rail sm-easyedapro:SMA_L4.4-W2.8-LS5.4-RD': 'Diode_SMD:SMA',
    '5v rail sm-easyedapro:SMA_L4.3-W2.6-LS5.0-RD': 'Diode_SMD:SMA',
    '5v rail sm-easyedapro:SMB_L4.6-W3.6-LS5.4-RD': 'Diode_SMD:SMB',

    '5v rail sm-easyedapro:SO-8_L4.9-W3.9-P1.27-LS5.9-BL': 'Package_SO:SOIC-8_3.9x4.9mm_P1.27mm',
    '5v rail sm-easyedapro:MSOP-10_L3.0-W3.0-P0.50-LS5.0-BL': 'Package_SO:MSOP-10_3x3mm_P0.5mm',
    '5v rail sm-easyedapro:TSSOP-16_L5.0-W4.4-P0.65-LS6.4-BL': 'Package_SO:TSSOP-16_4.4x5mm_P0.65mm',
    '5v rail sm-easyedapro:TSSOP-28_L9.7-W4.4-P0.65-LS6.4-TL': 'Package_SO:TSSOP-28_4.4x9.7mm_P0.65mm',
    '5v rail sm-easyedapro:VSSOP-8_L3.0-W3.0-P0.65-LS5.0-BL': 'Package_SO:VSSOP-8_3.0x3.0mm_P0.65mm',
    '5v rail sm-easyedapro:VSSOP-10_L3.0-W3.0-P0.50-LS4.9-BL': 'Package_SO:VSSOP-10_3.0x3.0mm_P0.5mm',

    '5v rail sm-easyedapro:QFN-16_L4.0-W4.0-P0.65-TL-EP2.2': 'Package_DFN_QFN:QFN-16-1EP_4x4mm_P0.65mm_EP2.2x2.2mm',
    '5v rail sm-easyedapro:QFN-16_L3.0-W3.0-P0.50-BL-EP1.7': 'Package_DFN_QFN:QFN-16-1EP_3x3mm_P0.5mm_EP1.7x1.7mm',
    '5v rail sm-easyedapro:TQFN-16_L3.0-W3.0-P0.50-BL-EP1.7': 'Package_DFN_QFN:QFN-16-1EP_3x3mm_P0.5mm_EP1.7x1.7mm',

    '5v rail sm-easyedapro:LGA-14L_L3.0-W2.5-P0.50-TL': 'Package_LGA:LGA-14_3x2.5mm_P0.5mm',
    '5v rail sm-easyedapro:TQFP-48_L7.0-W7.0-P0.50-LS9.0-TL': 'Package_QFP:TQFP-48_7x7mm_P0.5mm',
}

changed_files = 0
replacement_count = 0
for file_path in FILES:
    if not file_path.exists():
        continue
    text = file_path.read_text(encoding='utf-8', errors='ignore')
    original = text

    for old, new in MAP.items():
        matches = text.count(f'"{old}"')
        if matches:
            text = text.replace(f'"{old}"', f'"{new}"')
            replacement_count += matches

    if text != original:
        file_path.write_text(text, encoding='utf-8')
        changed_files += 1

print(f'changed_files: {changed_files}')
print(f'replacements: {replacement_count}')
