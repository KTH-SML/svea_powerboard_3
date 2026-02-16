#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

MAP = {
    "5v rail sm-easyedapro:R0201": "Resistor_SMD:R_0201_0603Metric",
    "5v rail sm-easyedapro:R0402": "Resistor_SMD:R_0402_1005Metric",
    "5v rail sm-easyedapro:R0603": "Resistor_SMD:R_0603_1608Metric",
    "5v rail sm-easyedapro:R0805": "Resistor_SMD:R_0805_2012Metric",
    "5v rail sm-easyedapro:R1206": "Resistor_SMD:R_1206_3216Metric",
    "5v rail sm-easyedapro:R1210": "Resistor_SMD:R_1210_3225Metric",
    "5v rail sm-easyedapro:R2010": "Resistor_SMD:R_2010_5025Metric",
    "5v rail sm-easyedapro:R2512": "Resistor_SMD:R_2512_6332Metric",
    "5v rail sm-easyedapro:C0201": "Capacitor_SMD:C_0201_0603Metric",
    "5v rail sm-easyedapro:C0402": "Capacitor_SMD:C_0402_1005Metric",
    "5v rail sm-easyedapro:C0603": "Capacitor_SMD:C_0603_1608Metric",
    "5v rail sm-easyedapro:C0805": "Capacitor_SMD:C_0805_2012Metric",
    "5v rail sm-easyedapro:C1206": "Capacitor_SMD:C_1206_3216Metric",
    "5v rail sm-easyedapro:C1210": "Capacitor_SMD:C_1210_3225Metric",
    "5v rail sm-easyedapro:C2220": "Capacitor_SMD:C_2220_5750Metric",
    "5v rail sm-easyedapro:L0603": "Inductor_SMD:L_0603_1608Metric",
    "5v rail sm-easyedapro:SOT-23-3_L3.0-W1.7-P0.95-LS2.9-BR": "Package_TO_SOT_SMD:SOT-23",
    "5v rail sm-easyedapro:SOT-23-3_L2.9-W1.3-P1.90-LS2.4-BR": "Package_TO_SOT_SMD:SOT-23",
    "5v rail sm-easyedapro:SOT-23_L2.9-W1.3-P1.90-LS2.4-BR": "Package_TO_SOT_SMD:SOT-23",
    "5v rail sm-easyedapro:SOT-23-5_L2.9-W1.6-P0.95-LS2.9-BL": "Package_TO_SOT_SMD:SOT-23-5",
    "5v rail sm-easyedapro:TSOT-23-5_L2.9-W1.6-P0.95-LS2.8-BL": "Package_TO_SOT_SMD:TSOT-23-5",
    "5v rail sm-easyedapro:SOT-23-6_L2.9-W1.6-P0.95-LS2.8-BL": "Package_TO_SOT_SMD:SOT-23-6",
    "5v rail sm-easyedapro:TSOT-23-6_L2.9-W1.6-P0.95-LS2.8-BL": "Package_TO_SOT_SMD:TSOT-23-6",
    "5v rail sm-easyedapro:SOT-353_L2.1-W1.3-P0.65-LS2.3-BL": "Package_TO_SOT_SMD:SOT-353_SC-70-5",
    "5v rail sm-easyedapro:SOT-223-3_L6.5-W3.4-P2.30-LS7.0-BR": "Package_TO_SOT_SMD:SOT-223-3_TabPin2",
    "5v rail sm-easyedapro:TO-252-2_L6.6-W6.1-P4.58-LS9.9-TL": "Package_TO_SOT_SMD:TO-252-2",
    "5v rail sm-easyedapro:TO-263-2_L10.1-W8.8-P5.08-LS15.4-TL": "Package_TO_SOT_SMD:TO-263-2_TabPin2",
    "5v rail sm-easyedapro:SOD-123_L2.8-W1.8-LS3.7-RD": "Diode_SMD:SOD-123",
    "5v rail sm-easyedapro:SOD-123_L2.7-W1.6-LS3.7-RD": "Diode_SMD:SOD-123",
    "5v rail sm-easyedapro:SOD-123_L2.7-W1.6-LS3.7-FD": "Diode_SMD:SOD-123",
    "5v rail sm-easyedapro:SOD-123F_L2.8-W1.8-LS3.7-RD": "Diode_SMD:SOD-123F",
    "5v rail sm-easyedapro:SOD-123FL_L2.8-W1.8-LS3.6-RD": "Diode_SMD:SOD-123FL",
    "5v rail sm-easyedapro:SOD-128_L3.7-W2.5-LS4.7-RD": "Diode_SMD:SOD-128",
    "5v rail sm-easyedapro:SOD-323_L1.8-W1.3-LS2.5-RD": "Diode_SMD:SOD-323",
    "5v rail sm-easyedapro:SMA_L4.4-W2.6-LS5.0-RD": "Diode_SMD:SMA",
    "5v rail sm-easyedapro:SMA_L4.4-W2.8-LS5.4-RD": "Diode_SMD:SMA",
    "5v rail sm-easyedapro:SMA_L4.3-W2.6-LS5.0-RD": "Diode_SMD:SMA",
    "5v rail sm-easyedapro:SMB_L4.6-W3.6-LS5.4-RD": "Diode_SMD:SMB",
    "5v rail sm-easyedapro:SO-8_L4.9-W3.9-P1.27-LS5.9-BL": "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm",
    "5v rail sm-easyedapro:MSOP-10_L3.0-W3.0-P0.50-LS5.0-BL": "Package_SO:MSOP-10_3x3mm_P0.5mm",
    "5v rail sm-easyedapro:TSSOP-16_L5.0-W4.4-P0.65-LS6.4-BL": "Package_SO:TSSOP-16_4.4x5mm_P0.65mm",
    "5v rail sm-easyedapro:TSSOP-28_L9.7-W4.4-P0.65-LS6.4-TL": "Package_SO:TSSOP-28_4.4x9.7mm_P0.65mm",
    "5v rail sm-easyedapro:VSSOP-8_L3.0-W3.0-P0.65-LS5.0-BL": "Package_SO:VSSOP-8_3.0x3.0mm_P0.65mm",
    "5v rail sm-easyedapro:VSSOP-10_L3.0-W3.0-P0.50-LS4.9-BL": "Package_SO:VSSOP-10_3.0x3.0mm_P0.5mm",
    "5v rail sm-easyedapro:QFN-16_L4.0-W4.0-P0.65-TL-EP2.2": "Package_DFN_QFN:QFN-16-1EP_4x4mm_P0.65mm_EP2.2x2.2mm",
    "5v rail sm-easyedapro:QFN-16_L3.0-W3.0-P0.50-BL-EP1.7": "Package_DFN_QFN:QFN-16-1EP_3x3mm_P0.5mm_EP1.7x1.7mm",
    "5v rail sm-easyedapro:TQFN-16_L3.0-W3.0-P0.50-BL-EP1.7": "Package_DFN_QFN:QFN-16-1EP_3x3mm_P0.5mm_EP1.7x1.7mm",
    "5v rail sm-easyedapro:LGA-14L_L3.0-W2.5-P0.50-TL": "Package_LGA:LGA-14_3x2.5mm_P0.5mm",
    "5v rail sm-easyedapro:TQFP-48_L7.0-W7.0-P0.50-LS9.0-TL": "Package_QFP:TQFP-48_7x7mm_P0.5mm",
    "5v rail sm-easyedapro:CAP-TH_BD13.0-P5.00-D0.6-FD": "Capacitor_THT:CP_Radial_D13.0mm_P5.00mm",
    "5v rail sm-easyedapro:F1206": "Fuse:Fuse_1206_3216Metric",
    "5v rail sm-easyedapro:LED0603-RD_RED": "LED_SMD:LED_0603_1608Metric",
    "5v rail sm-easyedapro:CONN-TH_2P-P3.96_VH3.96-2AW": "Connector_JST:JST_VH_B2P-VH_1x02_P3.96mm_Vertical",
    "5v rail sm-easyedapro:CONN-TH_2P-P2.50_HX25003-2A": "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical",
    "5v rail sm-easyedapro:CONN-TH_B2B-XH-A-LF-SN": "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical",
    "5v rail sm-easyedapro:CONN-TH_4P-P2.50_ZX-XH2.54-4PWZ": "Connector_JST:JST_XH_B4B-XH-A_1x04_P2.50mm_Vertical",
    "5v rail sm-easyedapro:CONN-TH_B4B-PH-K-S": "Connector_JST:JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical",
    "5v rail sm-easyedapro:CONN-TH_ZX-VH3.96-4PWZ": "Connector_JST:JST_VH_B4P-VH_1x04_P3.96mm_Vertical",
    "5v rail sm-easyedapro:HDR-TH_26P-P2.54-V-M-R2-C13-S2.54": "Connector_PinHeader_2.54mm:PinHeader_2x13_P2.54mm_Vertical",
    "5v rail sm-easyedapro:HDR-TH_2P-P2.54-V-M": "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical",
    "5v rail sm-easyedapro:HDR-TH_9P-P2.54_C9900044301": "Connector_PinHeader_2.54mm:PinHeader_1x09_P2.54mm_Vertical",
}


def target_files(kicad_dir: Path) -> list[Path]:
    files: list[Path] = []
    files.extend(sorted(kicad_dir.rglob("*.kicad_sch")))
    pcb = kicad_dir / "svea_powerboard_rev3.kicad_pcb"
    if pcb.exists():
        files.append(pcb)
    return files


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    kicad_dir = repo / "hardware" / "kicad"
    files = target_files(kicad_dir)

    total_replacements = 0
    changed_files = 0

    for file_path in files:
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        original = text
        for old, new in MAP.items():
            count = text.count(f'"{old}"')
            if count:
                text = text.replace(f'"{old}"', f'"{new}"')
                total_replacements += count
        if text != original:
            file_path.write_text(text, encoding="utf-8")
            changed_files += 1

    print(f"kicad_dir: {kicad_dir}")
    print(f"target_files: {len(files)}")
    print(f"changed_files: {changed_files}")
    print(f"replacements: {total_replacements}")


if __name__ == "__main__":
    main()
