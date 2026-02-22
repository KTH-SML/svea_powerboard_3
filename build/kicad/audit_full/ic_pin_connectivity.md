# IC pin connectivity report

## U1 LSM6DSOXTR
- sheet: sheets/modules/01_Battery-System.kicad_sch (Battery System)
- datasheet: https://item.szlcsc.com/datasheet/LSM6DSOXTR/489350.html
  - pin 1 SDO/SA0 -> +3V3 :: C1(10uF), C103(100nF), C104(10uF), C117(100nF), C118(1uF), C126(1uF), C127(100nF), C131(470nF), C14(100nF), C15(1uF), ...
  - pin 2 SDX -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin 3 SCX -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin 4 INT1 -> IMU/INT1 :: R68(47Ω)
  - pin 5 VDDIO -> +3V3 :: C1(10uF), C103(100nF), C104(10uF), C117(100nF), C118(1uF), C126(1uF), C127(100nF), C131(470nF), C14(100nF), C15(1uF), ...
  - pin 6 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin 7 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin 8 VDD -> +3V3 :: C1(10uF), C103(100nF), C104(10uF), C117(100nF), C118(1uF), C126(1uF), C127(100nF), C131(470nF), C14(100nF), C15(1uF), ...
  - pin 9 INT2 -> IMU/INT2 :: R61(47Ω)
  - pin 10 OSC_AUX -> unconnected-(U1-OSC_AUX-Pad10) :: 
  - pin 11 SDO_AUX -> unconnected-(U1-SDO_AUX-Pad11) :: 
  - pin 12 CS -> Net-(U1-CS) :: R17(10kΩ)
  - pin 13 SCL -> Net-(U1-SCL) :: U3(~), U5(~)
  - pin 14 SDA -> Net-(U1-SDA) :: U2(~), U4(~)

## U10 PCAL6524HEAZ
- sheet: sheets/modules/01_Battery-System.kicad_sch (Battery System)
- datasheet: https://www.nxp.com/docs/en/data-sheet/PCAL6524DS.pdf
  - pin 1 P0_0 -> Net-(U10-P0_0) :: R19(47Ω)
  - pin 2 P0_1 -> Net-(U10-P0_1) :: R20(47Ω)
  - pin 3 P0_2 -> Net-(U10-P0_2) :: R21(47Ω)
  - pin 4 P0_3 -> Net-(U10-P0_3) :: R22(47Ω)
  - pin 5 P0_4 -> Net-(U10-P0_4) :: R23(47Ω)
  - pin 6 P0_5 -> Net-(U10-P0_5) :: R24(47Ω)
  - pin 7 P0_6 -> Net-(U10-P0_6) :: R25(47Ω)
  - pin 8 P0_7 -> Net-(U10-P0_7) :: R26(47Ω)
  - pin 9 P1_0 -> Net-(U10-P1_0) :: R27(47Ω)
  - pin 10 P1_1 -> Net-(U10-P1_1) :: R28(47Ω)
  - pin 11 P1_2 -> Net-(U10-P1_2) :: R29(47Ω)
  - pin 12 P1_3 -> Net-(U10-P1_3) :: R30(47Ω)
  - pin 13 P1_4 -> Net-(U10-P1_4) :: R31(47Ω)
  - pin 14 P1_5 -> Net-(U10-P1_5) :: R32(47Ω)
  - pin 15 P1_6 -> Net-(U10-P1_6) :: R33(47Ω)
  - pin 16 P1_7 -> Net-(U10-P1_7) :: R34(47Ω)
  - pin 17 P2_0 -> Net-(U10-P2_0) :: R60(47Ω)
  - pin 18 P2_1 -> Net-(U10-P2_1) :: R59(47Ω)
  - pin 19 P2_2 -> Net-(U10-P2_2) :: R58(47Ω)
  - pin 20 P2_3 -> Net-(U10-P2_3) :: R57(47Ω)
  - pin 21 P2_4 -> Net-(U10-P2_4) :: R56(47Ω)
  - pin 22 P2_5 -> Net-(U10-P2_5) :: R55(47Ω)
  - pin 23 P2_6 -> Net-(U10-P2_6) :: R54(47Ω)
  - pin 24 P2_7 -> Net-(U10-P2_7) :: R53(47Ω)
  - pin 25 VSS -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin 26 ADDR -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin 27 VDD(P) -> +3V3 :: C1(10uF), C103(100nF), C104(10uF), C117(100nF), C118(1uF), C126(1uF), C127(100nF), C131(470nF), C14(100nF), C15(1uF), ...
  - pin 28 RESET# -> unconnected-(U10-RESET#-Pad28) :: 
  - pin 29 SCL -> Net-(U10-SCL) :: U13(~), U15(~)
  - pin 30 SDA -> Net-(U10-SDA) :: U12(~), U14(~)
  - pin 31 VDD(I2C-bus) -> +3V3 :: C1(10uF), C103(100nF), C104(10uF), C117(100nF), C118(1uF), C126(1uF), C127(100nF), C131(470nF), C14(100nF), C15(1uF), ...
  - pin 32 INT# -> IO-Expander/Primary/INT :: R70(10kΩ), U20(X1270WV-2X08B-6TV01), U67(X1270WV-2X08B-6TV01)
  - pin 33 EP -> unconnected-(U10-EP-Pad33) :: 

## U11 PCAL6524HEAZ
- sheet: sheets/modules/01_Battery-System.kicad_sch (Battery System)
- datasheet: https://www.nxp.com/docs/en/data-sheet/PCAL6524DS.pdf
  - pin 1 P0_0 -> Net-(U11-P0_0) :: R35(47Ω)
  - pin 2 P0_1 -> Net-(U11-P0_1) :: R36(47Ω)
  - pin 3 P0_2 -> Net-(U11-P0_2) :: R37(47Ω)
  - pin 4 P0_3 -> Net-(U11-P0_3) :: R38(47Ω)
  - pin 5 P0_4 -> Net-(U11-P0_4) :: R39(47Ω)
  - pin 6 P0_5 -> Net-(U11-P0_5) :: R40(47Ω)
  - pin 7 P0_6 -> Net-(U11-P0_6) :: R41(47Ω)
  - pin 8 P0_7 -> Net-(U11-P0_7) :: R42(47Ω)
  - pin 9 P1_0 -> Net-(U11-P1_0) :: R43(47Ω)
  - pin 10 P1_1 -> Net-(U11-P1_1) :: R44(47Ω)
  - pin 11 P1_2 -> Net-(U11-P1_2) :: R45(47Ω)
  - pin 12 P1_3 -> Net-(U11-P1_3) :: R46(47Ω)
  - pin 13 P1_4 -> Net-(U11-P1_4) :: R47(47Ω)
  - pin 14 P1_5 -> Net-(U11-P1_5) :: R48(47Ω)
  - pin 15 P1_6 -> Net-(U11-P1_6) :: R49(47Ω)
  - pin 16 P1_7 -> Net-(U11-P1_7) :: R50(47Ω)
  - pin 17 P2_0 -> Net-(U11-P2_0) :: R67(47Ω)
  - pin 18 P2_1 -> Net-(U11-P2_1) :: R66(47Ω)
  - pin 19 P2_2 -> Net-(U11-P2_2) :: R65(47Ω)
  - pin 20 P2_3 -> Net-(U11-P2_3) :: R64(47Ω)
  - pin 21 P2_4 -> Net-(U11-P2_4) :: R63(47Ω)
  - pin 22 P2_5 -> Net-(U11-P2_5) :: R62(47Ω)
  - pin 23 P2_6 -> Net-(U11-P2_6) :: R61(47Ω)
  - pin 24 P2_7 -> Net-(U11-P2_7) :: R68(47Ω)
  - pin 25 VSS -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin 26 ADDR -> +3V3 :: C1(10uF), C103(100nF), C104(10uF), C117(100nF), C118(1uF), C126(1uF), C127(100nF), C131(470nF), C14(100nF), C15(1uF), ...
  - pin 27 VDD(P) -> +3V3 :: C1(10uF), C103(100nF), C104(10uF), C117(100nF), C118(1uF), C126(1uF), C127(100nF), C131(470nF), C14(100nF), C15(1uF), ...
  - pin 28 RESET# -> unconnected-(U11-RESET#-Pad28) :: 
  - pin 29 SCL -> Net-(U11-SCL) :: U17(~), U19(~)
  - pin 30 SDA -> Net-(U11-SDA) :: U16(~), U18(~)
  - pin 31 VDD(I2C-bus) -> +3V3 :: C1(10uF), C103(100nF), C104(10uF), C117(100nF), C118(1uF), C126(1uF), C127(100nF), C131(470nF), C14(100nF), C15(1uF), ...
  - pin 32 INT# -> IO-Expander/Secondary/INT :: R72(10kΩ)
  - pin 33 EP -> unconnected-(U11-EP-Pad33) :: 

## U22 CN3722
- sheet: ../charging/4_Charging-Buck.kicad_sch (Charger Buck Stage)
- datasheet: https://atta.szlcsc.com/upload/public/pdf/source/20161217/1481939130627.pdf
  - pin 1 VG -> Net-(U22-VG) :: C26(100nF)
  - pin 2 PGND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin 3 GND -> Net-(U22-GND) :: C28(470pF), C29(220nF), C30(100nF), R83(1MΩ), R84(0Ω)
  - pin 4 CHRG# -> Charger/CN3072/CHG-DONE :: C22(100nF), C25(100nF), R109(0603WAF1000T5E), R48(47Ω), R73(0603WAF1000T5E), R82(10k)
  - pin 5 DONE# -> Charger/CN3072/CHG-ACTIVE :: C24(100nF), C27(100nF), R109(0603WAF1000T5E), R49(47Ω), R73(0603WAF1000T5E), R74(10k)
  - pin 6 TEMP -> Net-(Q19-D) :: Q19(L2N7002SLLT1G), R81(10kΩ)
  - pin 7 MPPT -> Net-(U22-MPPT) :: R75(100kΩ), R76(5.76kΩ)
  - pin 8 COM1 -> Net-(U22-COM1) :: C28(470pF), R83(1MΩ)
  - pin 9 COM2 -> Net-(U22-COM2) :: R85(120Ω)
  - pin 10 FB -> Net-(U22-FB) :: C31(2pF), R88(105kΩ), R89(24.9kΩ)
  - pin 11 COM3 -> Net-(U22-COM3) :: C30(100nF)
  - pin 12 NC -> unconnected-(U22-NC-Pad12) :: 
  - pin 13 CSP -> Net-(U22-CSP) :: R86(60mΩ), R87(--), U23(15uH)
  - pin 14 BAT -> /Battery System/Battery Power Path/CHG+ :: C135(RVT1H220M0605), C31(2pF), D32(MMSZ5246B_R1_00001), Q13(IPT012N08N5(TOKMAS)), Q14(IPT012N08N5(TOKMAS)), Q15(ZXMP10A17GTA), R203(1MΩ), R86(60mΩ), R87(--), R88(105kΩ)
  - pin 15 VCC -> IN-CHARGING-VCC-LIMITED :: C20(22uF), C21(22uF), C23(100nF), C26(100nF), C33(1uF), D13(~), Q2(ME50P06-G), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), ...
  - pin 16 DRV -> Net-(Q2-G) :: Q2(ME50P06-G)

## U24 LM5050MKX-1/NOPB
- sheet: ../charging/highcurrendiodeor.kicad_sch (Ideal_Diode_OR_CHARGING_PORT)
- datasheet: https://www.ti.com/cn/lit/gpn/lm5050-1
  - pin 1 VS -> Net-(U24-VS) :: C34(100nF), R91(100Ω)
  - pin 2 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin 3 OFF -> Power/Charging-VCC-Limited-Diode/EN# :: R34(47Ω), R90(100kΩ)
  - pin 4 IN -> IN-CHARGING-VCC-LIMITED :: C20(22uF), C21(22uF), C23(100nF), C26(100nF), C33(1uF), D13(~), Q2(ME50P06-G), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), ...
  - pin 5 GATE -> Net-(Q3-G) :: Q3(CSD17577Q5A)
  - pin 6 OUT -> VCC :: C50(100uF), C51(4.7uF), C52(4.7uF), D7(SS36), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q5(CSD17577Q5A), ...

## U25 LM5050MKX-1/NOPB
- sheet: ../charging/highcurrendiodeor.kicad_sch (Ideal_Diode_OR_DC_PORT)
- datasheet: https://www.ti.com/cn/lit/gpn/lm5050-1
  - pin 1 VS -> Net-(U25-VS) :: C36(100nF), R93(100Ω)
  - pin 2 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin 3 OFF -> Power/DC20V-Diode/EN# :: R55(47Ω), R92(100kΩ)
  - pin 4 IN -> DC_BARREL_20V_PORT :: C35(1uF), D14(~), D4(SS36), Q4(CSD17577Q5A), Q4(CSD17577Q5A), Q4(CSD17577Q5A)
  - pin 5 GATE -> Net-(Q4-G) :: Q4(CSD17577Q5A)
  - pin 6 OUT -> /Battery System/Ideal_Diode_OR_DC_PORT/OUT :: C74(100nF), Q4(CSD17577Q5A), Q4(CSD17577Q5A), Q4(CSD17577Q5A), Q4(CSD17577Q5A), Q4(CSD17577Q5A), Q8(CSD17577Q5A), Q8(CSD17577Q5A), Q8(CSD17577Q5A), Q8(CSD17577Q5A), ...

## U26 LM5050MKX-1/NOPB
- sheet: ../charging/highcurrendiodeor.kicad_sch (Ideal_Diode_OR_PACK+_VCC)
- datasheet: https://www.ti.com/cn/lit/gpn/lm5050-1
  - pin 1 VS -> Net-(U26-VS) :: C38(100nF), R95(100Ω)
  - pin 2 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin 3 OFF -> Power/PACK+-VCC-Diode/EN# :: R56(47Ω), R94(100kΩ)
  - pin 4 IN -> PACK+ :: C125(100nF), C128(100nF), C13(4700uF), C37(1uF), C8(ERA16V4700M13X25), D15(~), D34(MMSZ5246B-7-F), D36(MMSZ5246B-7-F), Q14(IPT012N08N5(TOKMAS)), Q17(BSS123NH6327), ...
  - pin 5 GATE -> Net-(Q5-G) :: Q5(CSD17577Q5A)
  - pin 6 OUT -> VCC :: C50(100uF), C51(4.7uF), C52(4.7uF), D7(SS36), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q5(CSD17577Q5A), ...

## U30 MCP4725A0T-E/CH
- sheet: ../power/12v_LTM8055_BUCK.kicad_sch (12v_LTM8055_BUCK)
- datasheet: https://item.szlcsc.com/datasheet/MCP4725A0T-E%252FCH/155530.html
  - pin 1 VOUT -> Net-(U30-VOUT) :: 
  - pin 2 VSS -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin 3 VDD -> +3V3 :: C1(10uF), C103(100nF), C104(10uF), C117(100nF), C118(1uF), C126(1uF), C127(100nF), C131(470nF), C14(100nF), C15(1uF), ...
  - pin 4 SDA -> SDA_SLOW :: R52(4.7kΩ), U12(~), U16(~), U2(~), U31(ADS1115IDGST), U56(INA226AIDGSR), U56(INA226AIDGSR), U6(~), U64(BQ7694202PFBR), U65(INA226AIDGSR), ...
  - pin 5 SCL -> SCL_SLOW :: R51(4.7kΩ), U13(~), U17(~), U3(~), U31(ADS1115IDGST), U56(INA226AIDGSR), U56(INA226AIDGSR), U64(BQ7694202PFBR), U65(INA226AIDGSR), U65(INA226AIDGSR), ...
  - pin 6 A0 -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...

## U31 ADS1115IDGST
- sheet: ../power/12v_LTM8055_BUCK.kicad_sch (12v_LTM8055_BUCK)
- datasheet: https://www.ti.com/cn/lit/gpn/ads1113
  - pin 1 ADDR -> +3V3 :: C1(10uF), C103(100nF), C104(10uF), C117(100nF), C118(1uF), C126(1uF), C127(100nF), C131(470nF), C14(100nF), C15(1uF), ...
  - pin 2 ALERT/RDY -> Net-(U31-ALERT/RDY) :: R107(100Ω)
  - pin 3 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin 4 AIN0 -> eFuse/TPS16630/IMON :: R135(19.1Ω), U42(TPS16630RGER)
  - pin 5 AIN1 -> Power/12V-Buck/IINMON :: U33(LTM8055IY_PBF)
  - pin 6 AIN2 -> unconnected-(U31-AIN2-Pad6) :: 
  - pin 7 AIN3 -> Power/12V-Buck/IOUTMON :: U33(LTM8055IY_PBF)
  - pin 8 VDD -> +3V3 :: C1(10uF), C103(100nF), C104(10uF), C117(100nF), C118(1uF), C126(1uF), C127(100nF), C131(470nF), C14(100nF), C15(1uF), ...
  - pin 9 SDA -> SDA_SLOW :: R52(4.7kΩ), U12(~), U16(~), U2(~), U30(MCP4725A0T-E/CH), U56(INA226AIDGSR), U56(INA226AIDGSR), U6(~), U64(BQ7694202PFBR), U65(INA226AIDGSR), ...
  - pin 10 SCL -> SCL_SLOW :: R51(4.7kΩ), U13(~), U17(~), U3(~), U30(MCP4725A0T-E/CH), U56(INA226AIDGSR), U56(INA226AIDGSR), U64(BQ7694202PFBR), U65(INA226AIDGSR), U65(INA226AIDGSR), ...

## U33 LTM8055IY_PBF
- sheet: ../power/12v_LTM8055_BUCK.kicad_sch (12v_LTM8055_BUCK)
- datasheet: 
  - pin A1 VOUT -> Net-(C58-Pad2) :: C58(22uF), R111(100kΩ), R113(7mΩ), U34(68uF)
  - pin A10 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin A11 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin A2 VOUT -> Net-(C58-Pad2) :: C58(22uF), R111(100kΩ), R113(7mΩ), U34(68uF)
  - pin A3 VOUT -> Net-(C58-Pad2) :: C58(22uF), R111(100kΩ), R113(7mΩ), U34(68uF)
  - pin A4 VOUT -> Net-(C58-Pad2) :: C58(22uF), R111(100kΩ), R113(7mΩ), U34(68uF)
  - pin A5 VOUT -> Net-(C58-Pad2) :: C58(22uF), R111(100kΩ), R113(7mΩ), U34(68uF)
  - pin A6 VOUT -> Net-(C58-Pad2) :: C58(22uF), R111(100kΩ), R113(7mΩ), U34(68uF)
  - pin A7 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin A8 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin A9 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin B1 VOUT -> Net-(C58-Pad2) :: C58(22uF), R111(100kΩ), R113(7mΩ), U34(68uF)
  - pin B10 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin B11 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin B2 VOUT -> Net-(C58-Pad2) :: C58(22uF), R111(100kΩ), R113(7mΩ), U34(68uF)
  - pin B3 VOUT -> Net-(C58-Pad2) :: C58(22uF), R111(100kΩ), R113(7mΩ), U34(68uF)
  - pin B4 VOUT -> Net-(C58-Pad2) :: C58(22uF), R111(100kΩ), R113(7mΩ), U34(68uF)
  - pin B5 VOUT -> Net-(C58-Pad2) :: C58(22uF), R111(100kΩ), R113(7mΩ), U34(68uF)
  - pin B6 VOUT -> Net-(C58-Pad2) :: C58(22uF), R111(100kΩ), R113(7mΩ), U34(68uF)
  - pin B7 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin B8 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin B9 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin C1 VOUT -> Net-(C58-Pad2) :: C58(22uF), R111(100kΩ), R113(7mΩ), U34(68uF)
  - pin C10 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin C11 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin C2 VOUT -> Net-(C58-Pad2) :: C58(22uF), R111(100kΩ), R113(7mΩ), U34(68uF)
  - pin C3 VOUT -> Net-(C58-Pad2) :: C58(22uF), R111(100kΩ), R113(7mΩ), U34(68uF)
  - pin C4 VOUT -> Net-(C58-Pad2) :: C58(22uF), R111(100kΩ), R113(7mΩ), U34(68uF)
  - pin C5 VOUT -> Net-(C58-Pad2) :: C58(22uF), R111(100kΩ), R113(7mΩ), U34(68uF)
  - pin C6 VOUT -> Net-(C58-Pad2) :: C58(22uF), R111(100kΩ), R113(7mΩ), U34(68uF)
  - pin C7 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin C8 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin C9 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin D1 IOUT -> Net-(U33-IOUT) :: 
  - pin D10 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin D11 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin D2 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin D3 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin D4 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin D5 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin D6 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin D7 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin D8 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin D9 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin E1 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin E10 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin E11 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin E2 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin E3 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin E4 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin E5 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin E6 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin E7 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin E8 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin E9 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin F1 LL -> Net-(U32-A) :: C57(100nF), U32(~)
  - pin F10 SVIN -> VCC :: C50(100uF), C51(4.7uF), C52(4.7uF), D7(SS36), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q5(CSD17577Q5A), ...
  - pin F11 SVIN -> VCC :: C50(100uF), C51(4.7uF), C52(4.7uF), D7(SS36), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q5(CSD17577Q5A), ...
  - pin F2 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin F3 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin F4 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin F5 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin F6 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin F7 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin F8 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin F9 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin G1 CLKOUT -> unconnected-(U33-CLKOUT-PadG1) :: 
  - pin G10 VIN -> VCC :: C50(100uF), C51(4.7uF), C52(4.7uF), D7(SS36), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q5(CSD17577Q5A), ...
  - pin G11 VIN -> VCC :: C50(100uF), C51(4.7uF), C52(4.7uF), D7(SS36), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q5(CSD17577Q5A), ...
  - pin G2 MODE -> Net-(U32-B) :: U32(~)
  - pin G3 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin G4 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin G5 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin G6 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin G7 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin G8 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin G9 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin H1 RT -> Net-(U33-RT) :: R110(36.5kΩ)
  - pin H10 VIN -> VCC :: C50(100uF), C51(4.7uF), C52(4.7uF), D7(SS36), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q5(CSD17577Q5A), ...
  - pin H11 VIN -> VCC :: C50(100uF), C51(4.7uF), C52(4.7uF), D7(SS36), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q5(CSD17577Q5A), ...
  - pin H2 SYNC -> /Battery System/12v_LTM8055_BUCK/LTM8055-SYNC :: 
  - pin H3 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin H4 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin H5 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin H6 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin H7 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin H8 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin H9 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin J1 FB -> Net-(U33-FB) :: R111(100kΩ), R112(11kΩ)
  - pin J10 VIN -> VCC :: C50(100uF), C51(4.7uF), C52(4.7uF), D7(SS36), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q5(CSD17577Q5A), ...
  - pin J11 VIN -> VCC :: C50(100uF), C51(4.7uF), C52(4.7uF), D7(SS36), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q5(CSD17577Q5A), ...
  - pin J2 COMP -> unconnected-(U33-COMP-PadJ2) :: 
  - pin J3 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin J4 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin J5 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin J6 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin J7 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin J8 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin J9 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin K1 SS -> Net-(U33-SS) :: C55(220nF)
  - pin K10 VIN -> VCC :: C50(100uF), C51(4.7uF), C52(4.7uF), D7(SS36), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q5(CSD17577Q5A), ...
  - pin K11 VIN -> VCC :: C50(100uF), C51(4.7uF), C52(4.7uF), D7(SS36), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q5(CSD17577Q5A), ...
  - pin K2 CTL -> Net-(U33-CTL) :: 
  - pin K3 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin K4 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin K5 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin K6 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin K7 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin K8 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin K9 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin L1 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin L10 VIN -> VCC :: C50(100uF), C51(4.7uF), C52(4.7uF), D7(SS36), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q5(CSD17577Q5A), ...
  - pin L11 VIN -> VCC :: C50(100uF), C51(4.7uF), C52(4.7uF), D7(SS36), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q5(CSD17577Q5A), ...
  - pin L2 IOUTMON -> Power/12V-Buck/IOUTMON :: U31(ADS1115IDGST)
  - pin L3 IINMON -> Power/12V-Buck/IINMON :: U31(ADS1115IDGST)
  - pin L4 RUN -> Power/12V-Buck/EN :: R106(100kΩ), R32(47Ω)
  - pin L5 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin L6 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin L7 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin L8 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin L9 IIN -> Net-(U33-IIN) :: R108(0)

## U35 LM5050MKX-1/NOPB
- sheet: ../charging/highcurrendiodeor.kicad_sch (Ideal_Diode_OR_12V_BUCK)
- datasheet: https://www.ti.com/cn/lit/gpn/lm5050-1
  - pin 1 VS -> Net-(U35-VS) :: C62(100nF), R115(100Ω)
  - pin 2 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin 3 OFF -> Power/12V-Diode/EN# :: R114(100kΩ), R33(47Ω)
  - pin 4 IN -> /Battery System/12v_LTM8055_BUCK/OUT :: C59(47uF), C60(470uF), C61(1uF), D19(~), Q6(CSD17577Q5A), Q6(CSD17577Q5A), Q6(CSD17577Q5A), R113(7mΩ)
  - pin 5 GATE -> Net-(Q6-G) :: Q6(CSD17577Q5A)
  - pin 6 OUT -> +12V :: C5(10uF), C6(100nF), C81(100nF), C82(470uF), C84(100nF), C85(470uF), D3(SMF13A), Q6(CSD17577Q5A), Q6(CSD17577Q5A), Q6(CSD17577Q5A), ...

## U36 LM5050MKX-1/NOPB
- sheet: ../charging/highcurrendiodeor.kicad_sch (Ideal_Diode_OR_SERVO)
- datasheet: https://www.ti.com/cn/lit/gpn/lm5050-1
  - pin 1 VS -> Net-(U36-VS) :: C64(100nF), R117(100Ω)
  - pin 2 GND -> SERVO-GND :: C10(HGC1206R5107M100NSPJ), C11(HGC1206R5107M100NSPJ), C12(HGC1206R5107M100NSPJ), C63(1uF), C64(100nF), C65(10uF), C66(10uF), C68(100uF), C69(47uF), C70(47uF), ...
  - pin 3 OFF -> Servo/VCC-Diode/EN# :: R116(100kΩ), R58(47Ω)
  - pin 4 IN -> /Battery System/Ideal_Diode_OR_SERVO/IN :: C10(HGC1206R5107M100NSPJ), C11(HGC1206R5107M100NSPJ), C12(HGC1206R5107M100NSPJ), C63(1uF), C67(22pF), C68(100uF), C69(47uF), C70(47uF), C71(47uF), C9(25YXJ1000M10X20), ...
  - pin 5 GATE -> Net-(Q7-G) :: Q7(CSD17577Q5A)
  - pin 6 OUT -> /Battery System/INA226_SINGLE_CURR_SENSOR_SERVO/VIN+ :: Q7(CSD17577Q5A), Q7(CSD17577Q5A), Q7(CSD17577Q5A), Q7(CSD17577Q5A), Q7(CSD17577Q5A), R117(100Ω), R16(RLM25FEER005)

## U37 TPSM63610RDFR
- sheet: ../power/28_Power-servo.kicad_sch (Servo Power Buck)
- datasheet: https://item.szlcsc.com/datasheet/TPSM63610RDFR/8092608.html
  - pin 1 VIN1 -> /Battery System/Servo Power Buck/IN :: C65(10uF), C66(10uF)
  - pin 2 RBOOT -> Net-(U37-RBOOT) :: R123(100Ω), U38(~)
  - pin 3 CBOOT -> Net-(U37-CBOOT) :: R123(100Ω), U38(~)
  - pin 4 SW -> unconnected-(U37-SW-Pad4) :: 
  - pin 5 VLDOIN -> /Battery System/Ideal_Diode_OR_SERVO/IN :: C10(HGC1206R5107M100NSPJ), C11(HGC1206R5107M100NSPJ), C12(HGC1206R5107M100NSPJ), C63(1uF), C67(22pF), C68(100uF), C69(47uF), C70(47uF), C71(47uF), C9(25YXJ1000M10X20), ...
  - pin 6 VCC -> unconnected-(U37-VCC-Pad6) :: 
  - pin 7 AGND -> GNDA :: R118(26.7kΩ), R119(100kΩ), R121(100kΩ), R125(20kΩ)
  - pin 8 FB -> Net-(U37-FB) :: C67(22pF), R124(100kΩ), R125(20kΩ)
  - pin 9 VOUT1 -> /Battery System/Ideal_Diode_OR_SERVO/IN :: C10(HGC1206R5107M100NSPJ), C11(HGC1206R5107M100NSPJ), C12(HGC1206R5107M100NSPJ), C63(1uF), C67(22pF), C68(100uF), C69(47uF), C70(47uF), C71(47uF), C9(25YXJ1000M10X20), ...
  - pin 10 VOUT2 -> /Battery System/Ideal_Diode_OR_SERVO/IN :: C10(HGC1206R5107M100NSPJ), C11(HGC1206R5107M100NSPJ), C12(HGC1206R5107M100NSPJ), C63(1uF), C67(22pF), C68(100uF), C69(47uF), C70(47uF), C71(47uF), C9(25YXJ1000M10X20), ...
  - pin 11 AGND -> GNDA :: R118(26.7kΩ), R119(100kΩ), R121(100kΩ), R125(20kΩ)
  - pin 12 RT -> Net-(U37-RT) :: R118(26.7kΩ)
  - pin 13 PG -> Servo/TPS/PGOOD :: R122(47kΩ), R30(47Ω)
  - pin 14 SPSP -> Net-(JP4-B) :: 
  - pin 15 MODE -> Net-(U37-MODE) :: R119(100kΩ)
  - pin 16 NC -> SERVO-GND :: C10(HGC1206R5107M100NSPJ), C11(HGC1206R5107M100NSPJ), C12(HGC1206R5107M100NSPJ), C63(1uF), C64(100nF), C65(10uF), C66(10uF), C68(100uF), C69(47uF), C70(47uF), ...
  - pin 17 EN -> Servo/TPS/EN :: R121(100kΩ), R29(47Ω)
  - pin 18 VIN2 -> /Battery System/Servo Power Buck/IN :: C65(10uF), C66(10uF)
  - pin 19 PGND -> SERVO-GND :: C10(HGC1206R5107M100NSPJ), C11(HGC1206R5107M100NSPJ), C12(HGC1206R5107M100NSPJ), C63(1uF), C64(100nF), C65(10uF), C66(10uF), C68(100uF), C69(47uF), C70(47uF), ...
  - pin 20 PGND -> SERVO-GND :: C10(HGC1206R5107M100NSPJ), C11(HGC1206R5107M100NSPJ), C12(HGC1206R5107M100NSPJ), C63(1uF), C64(100nF), C65(10uF), C66(10uF), C68(100uF), C69(47uF), C70(47uF), ...
  - pin 21 AGND -> GNDA :: R118(26.7kΩ), R119(100kΩ), R121(100kΩ), R125(20kΩ)
  - pin 22 AGND -> GNDA :: R118(26.7kΩ), R119(100kΩ), R121(100kΩ), R125(20kΩ)

## U39 LM5050MKX-1/NOPB
- sheet: ../charging/highcurrendiodeor.kicad_sch (Ideal_Diode_OR_USBC)
- datasheet: https://www.ti.com/cn/lit/gpn/lm5050-1
  - pin 1 VS -> Net-(U39-VS) :: C73(100nF), R127(100Ω)
  - pin 2 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin 3 OFF -> Power/USBC-Diode/EN# :: R126(100kΩ), R57(47Ω)
  - pin 4 IN -> /Battery System/USBC_VCC :: C72(1uF), D21(~), Q8(CSD17577Q5A), Q8(CSD17577Q5A), Q8(CSD17577Q5A), Q9(DMP3028LK3-13)
  - pin 5 GATE -> Net-(Q8-G) :: Q8(CSD17577Q5A)
  - pin 6 OUT -> /Battery System/Ideal_Diode_OR_DC_PORT/OUT :: C74(100nF), Q4(CSD17577Q5A), Q4(CSD17577Q5A), Q4(CSD17577Q5A), Q4(CSD17577Q5A), Q4(CSD17577Q5A), Q8(CSD17577Q5A), Q8(CSD17577Q5A), Q8(CSD17577Q5A), Q8(CSD17577Q5A), ...

## U42 TPS16630RGER
- sheet: ../charging/TPS16630RGER_CHARGING_EFUSE.kicad_sch (TPS16630RGER_CHARGING_EFUSE)
- datasheet: https://www.ti.com/cn/lit/gpn/tps1663
  - pin 1 IN -> /Battery System/Ideal_Diode_OR_DC_PORT/OUT :: C74(100nF), Q4(CSD17577Q5A), Q4(CSD17577Q5A), Q4(CSD17577Q5A), Q4(CSD17577Q5A), Q4(CSD17577Q5A), Q8(CSD17577Q5A), Q8(CSD17577Q5A), Q8(CSD17577Q5A), Q8(CSD17577Q5A), ...
  - pin 2 IN -> /Battery System/Ideal_Diode_OR_DC_PORT/OUT :: C74(100nF), Q4(CSD17577Q5A), Q4(CSD17577Q5A), Q4(CSD17577Q5A), Q4(CSD17577Q5A), Q4(CSD17577Q5A), Q8(CSD17577Q5A), Q8(CSD17577Q5A), Q8(CSD17577Q5A), Q8(CSD17577Q5A), ...
  - pin 3 N.C -> unconnected-(U42-N.C-Pad3) :: 
  - pin 4 N.C -> unconnected-(U42-N.C-Pad4) :: 
  - pin 5 P_IN -> /Battery System/Ideal_Diode_OR_DC_PORT/OUT :: C74(100nF), Q4(CSD17577Q5A), Q4(CSD17577Q5A), Q4(CSD17577Q5A), Q4(CSD17577Q5A), Q4(CSD17577Q5A), Q8(CSD17577Q5A), Q8(CSD17577Q5A), Q8(CSD17577Q5A), Q8(CSD17577Q5A), ...
  - pin 6 UVLO -> Net-(U42-UVLO) :: R130(442kΩ), R131(11kΩ)
  - pin 7 OVP -> Net-(U42-OVP) :: R131(11kΩ), R132(20kΩ)
  - pin 8 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin 9 dVdT -> Net-(U42-dVdT) :: C75(22nF)
  - pin 10 ILIM -> Net-(U42-ILIM) :: R128(3.92kΩ)
  - pin 11 MODE -> Net-(U41-B) :: U41(~)
  - pin 12 SHDN# -> eFuse/TPS16630/SHDN :: R133(100kΩ), R54(47Ω)
  - pin 13 IMON -> eFuse/TPS16630/IMON :: R135(19.1Ω), U31(ADS1115IDGST)
  - pin 14 FLT# -> eFuse/TPS16630/FAULT :: R134(100kΩ), R53(47Ω)
  - pin 15 N.C -> unconnected-(U42-N.C-Pad15) :: 
  - pin 16 PGOOD -> eFuse/TPS16630/PGOOD :: R60(47Ω)
  - pin 17 OUT -> IN-CHARGING-VCC-LIMITED :: C20(22uF), C21(22uF), C23(100nF), C26(100nF), C33(1uF), D13(~), Q2(ME50P06-G), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), ...
  - pin 18 OUT -> IN-CHARGING-VCC-LIMITED :: C20(22uF), C21(22uF), C23(100nF), C26(100nF), C33(1uF), D13(~), Q2(ME50P06-G), Q3(CSD17577Q5A), Q3(CSD17577Q5A), Q3(CSD17577Q5A), ...
  - pin 19 N.C -> unconnected-(U42-N.C-Pad19) :: 
  - pin 20 N.C -> unconnected-(U42-N.C-Pad20) :: 
  - pin 21 N.C -> unconnected-(U42-N.C-Pad21) :: 
  - pin 22 N.C -> unconnected-(U42-N.C-Pad22) :: 
  - pin 23 N.C -> unconnected-(U42-N.C-Pad23) :: 
  - pin 24 N.C -> unconnected-(U42-N.C-Pad24) :: 
  - pin 25 EP -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...

## U45 HUSB238A-BB001-QN16R
- sheet: ../charging/23_Charging-USB-C-Port.kicad_sch (USB-C Input)
- datasheet: https://item.szlcsc.com/datasheet/HUSB238A-BB001-QN16R/26562539.html
  - pin 1 D+ -> Net-(D22-IO3) :: D22(TPD4E02B04DQAR)
  - pin 2 D- -> Net-(D22-IO4) :: D22(TPD4E02B04DQAR)
  - pin 3 CC1 -> Net-(D22-IO1) :: D22(TPD4E02B04DQAR)
  - pin 4 CC2 -> Net-(D22-IO2) :: D22(TPD4E02B04DQAR)
  - pin 5 VDD -> Net-(U45-VDD) :: C77(1uF), R138(909kΩ), R141(10Ω)
  - pin 6 DBG_N -> Net-(U45-DBG_N) :: R140(909kΩ)
  - pin 7 EN_HVDCP/OUT1 -> Net-(U45-EN_HVDCP/OUT1) :: R138(909kΩ)
  - pin 8 ADDR/ORIENT -> Net-(U45-ADDR/ORIENT) :: R144(10kΩ)
  - pin 9 SDA/SNK_VSET -> Net-(U44-B) :: U44(~)
  - pin 10 SCL/SNK_ISET -> Net-(U43-B) :: U43(~)
  - pin 11 INT_N -> USB-C/HUSB238A/INT :: R145(100kΩ), R24(47Ω)
  - pin 12 EN_N -> USB-C/HUSB238A/EN# :: R139(100kΩ), R21(47Ω)
  - pin 13 FAULT/OUT2 -> USB-C/HUSB238A/FAULT-OUT2 :: R66(47Ω)
  - pin 14 FLGIN -> unconnected-(U45-FLGIN-Pad14) :: 
  - pin 15 GATE -> Net-(U45-GATE) :: R143(30kΩ)
  - pin 16 VBUS -> Net-(D23-K) :: C76(1uF), D23(SMBJ30A), D24(BZT52C15), Q9(DMP3028LK3-13), R141(10Ω), R142(100kΩ)
  - pin 17 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...

## U47 MT9700-N
- sheet: ../connectors/mt9700-efuse.kicad_sch (mt9700-efuse)
- datasheet: https://item.szlcsc.com/datasheet/MT9700-N/44491709.html
  - pin 1 VOUT -> /Battery System/ServoConnectors/3v3 :: C80(100nF), U48(150uF)
  - pin 2 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin 3 SET -> /Battery System/mt9700-efuse/SET :: R15(11.3kΩ)
  - pin 4 EN -> Net-(U47-EN) :: R146(47Ω), R147(100kΩ), R148(4.7kΩ)
  - pin 5 VIN -> +3V3 :: C1(10uF), C103(100nF), C104(10uF), C117(100nF), C118(1uF), C126(1uF), C127(100nF), C131(470nF), C14(100nF), C15(1uF), ...

## U49 74AHCT1G125GW,125-JSM
- sheet: ../mcu/33_Microcontroller-leds.kicad_sch (Status LEDs)
- datasheet: https://item.szlcsc.com/datasheet/74AHCT1G125GW%252C125-JSM/56091373.html
  - pin 1 OE# -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin 2 A -> LED/WS2815/DATA :: U67(X1270WV-2X08B-6TV01)
  - pin 3 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin 4 Y -> Net-(U49-Y) :: R149(220Ω)
  - pin 5 VCC -> +5V :: C133(470nF), C19(470nF), C3(10uF), C4(100nF), C83(100nF), D2(SMF6.0A), R3(16mΩ), U20(X1270WV-2X08B-6TV01), U67(X1270WV-2X08B-6TV01)

## U50 WS2815F
- sheet: ../mcu/33_Microcontroller-leds.kicad_sch (Status LEDs)
- datasheet: https://item.szlcsc.com/datasheet/WS2815F/23859553.html
  - pin 1 NC -> unconnected-(U50-NC-Pad1) :: 
  - pin 2 VDD -> +12V :: C5(10uF), C6(100nF), C81(100nF), C82(470uF), C84(100nF), C85(470uF), D3(SMF13A), Q6(CSD17577Q5A), Q6(CSD17577Q5A), Q6(CSD17577Q5A), ...
  - pin 3 DO -> Net-(U50-DO) :: U51(WS2815F)
  - pin 4 DIN1 -> Net-(U50-DIN1) :: R149(220Ω)
  - pin 5 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin 6 DIN2 -> unconnected-(U50-DIN2-Pad6) :: 

## U51 WS2815F
- sheet: ../mcu/33_Microcontroller-leds.kicad_sch (Status LEDs)
- datasheet: https://item.szlcsc.com/datasheet/WS2815F/23859553.html
  - pin 1 NC -> unconnected-(U51-NC-Pad1) :: 
  - pin 2 VDD -> +12V :: C5(10uF), C6(100nF), C81(100nF), C82(470uF), C84(100nF), C85(470uF), D3(SMF13A), Q6(CSD17577Q5A), Q6(CSD17577Q5A), Q6(CSD17577Q5A), ...
  - pin 3 DO -> Net-(U51-DO) :: U52(WS2815F)
  - pin 4 DIN1 -> Net-(U50-DO) :: U50(WS2815F)
  - pin 5 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin 6 DIN2 -> unconnected-(U51-DIN2-Pad6) :: 

## U52 WS2815F
- sheet: ../mcu/33_Microcontroller-leds.kicad_sch (Status LEDs)
- datasheet: https://item.szlcsc.com/datasheet/WS2815F/23859553.html
  - pin 1 NC -> unconnected-(U52-NC-Pad1) :: 
  - pin 2 VDD -> +12V :: C5(10uF), C6(100nF), C81(100nF), C82(470uF), C84(100nF), C85(470uF), D3(SMF13A), Q6(CSD17577Q5A), Q6(CSD17577Q5A), Q6(CSD17577Q5A), ...
  - pin 3 DO -> Net-(U52-DO) :: U54(WS2815F)
  - pin 4 DIN1 -> Net-(U51-DO) :: U51(WS2815F)
  - pin 5 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin 6 DIN2 -> unconnected-(U52-DIN2-Pad6) :: 

## U54 WS2815F
- sheet: ../mcu/33_Microcontroller-leds.kicad_sch (Status LEDs)
- datasheet: https://item.szlcsc.com/datasheet/WS2815F/23859553.html
  - pin 1 NC -> unconnected-(U54-NC-Pad1) :: 
  - pin 2 VDD -> +12V :: C5(10uF), C6(100nF), C81(100nF), C82(470uF), C84(100nF), C85(470uF), D3(SMF13A), Q6(CSD17577Q5A), Q6(CSD17577Q5A), Q6(CSD17577Q5A), ...
  - pin 3 DO -> Net-(U54-DO) :: U55(WS2815F)
  - pin 4 DIN1 -> Net-(U52-DO) :: U52(WS2815F)
  - pin 5 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin 6 DIN2 -> unconnected-(U54-DIN2-Pad6) :: 

## U55 WS2815F
- sheet: ../mcu/33_Microcontroller-leds.kicad_sch (Status LEDs)
- datasheet: https://item.szlcsc.com/datasheet/WS2815F/23859553.html
  - pin 1 NC -> unconnected-(U55-NC-Pad1) :: 
  - pin 2 VDD -> +12V :: C5(10uF), C6(100nF), C81(100nF), C82(470uF), C84(100nF), C85(470uF), D3(SMF13A), Q6(CSD17577Q5A), Q6(CSD17577Q5A), Q6(CSD17577Q5A), ...
  - pin 3 DO -> unconnected-(U55-DO-Pad3) :: 
  - pin 4 DIN1 -> Net-(U54-DO) :: U54(WS2815F)
  - pin 5 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin 6 DIN2 -> unconnected-(U55-DIN2-Pad6) :: 

## U56 INA226AIDGSR
- sheet: ../connectors/INA226_SINGLE_CURR_SENSOR.kicad_sch (INA226_SINGLE_CURR_SENSOR_ESC)
- datasheet: https://item.szlcsc.com/datasheet/INA226AIDGSR/50860.html
  - pin 1 A1 -> SCL_SLOW :: R51(4.7kΩ), U13(~), U17(~), U3(~), U30(MCP4725A0T-E/CH), U31(ADS1115IDGST), U64(BQ7694202PFBR), U65(INA226AIDGSR), U65(INA226AIDGSR), U65(INA226AIDGSR), ...
  - pin 2 A0 -> SDA_SLOW :: R52(4.7kΩ), U12(~), U16(~), U2(~), U30(MCP4725A0T-E/CH), U31(ADS1115IDGST), U6(~), U64(BQ7694202PFBR), U65(INA226AIDGSR), U67(X1270WV-2X08B-6TV01)
  - pin 3 Alert -> Current/INA226-ESC-0x4E/ALERT :: R43(47Ω)
  - pin 4 SDA -> SDA_SLOW :: R52(4.7kΩ), U12(~), U16(~), U2(~), U30(MCP4725A0T-E/CH), U31(ADS1115IDGST), U6(~), U64(BQ7694202PFBR), U65(INA226AIDGSR), U67(X1270WV-2X08B-6TV01)
  - pin 5 SCL -> SCL_SLOW :: R51(4.7kΩ), U13(~), U17(~), U3(~), U30(MCP4725A0T-E/CH), U31(ADS1115IDGST), U64(BQ7694202PFBR), U65(INA226AIDGSR), U65(INA226AIDGSR), U65(INA226AIDGSR), ...
  - pin 6 VS+ -> +3V3 :: C1(10uF), C103(100nF), C104(10uF), C117(100nF), C118(1uF), C126(1uF), C127(100nF), C131(470nF), C14(100nF), C15(1uF), ...
  - pin 7 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin 8 VBUS -> /Battery System/INA226_SINGLE_CURR_SENSOR_ESC/VIN_P :: 
  - pin 9 VIN- -> /Battery System/INA226_SINGLE_CURR_SENSOR_ESC/VIN_N :: 
  - pin 10 VIN+ -> /Battery System/INA226_SINGLE_CURR_SENSOR_ESC/VIN_P :: 

## U57 TPSM33625RDNR
- sheet: ../power/Power-3v3.kicad_sch (3v3 rail)
- datasheet: https://item.szlcsc.com/datasheet/TPSM33625RDNR/8040204.html
  - pin 1 PGOOD -> Power/3V3/PGOOD :: R22(47Ω)
  - pin 2 EN -> Power/3V3/EN :: R152(100kΩ), R25(47Ω)
  - pin 3 VIN -> /Battery System/3v3 rail/VCC :: C92(100nF), C93(4.7uF), C97(100nF), C98(4.7uF), C99(47uF), D4(SS36), D5(SS36), D6(SS36), D7(SS36), R157(100kΩ), ...
  - pin 4 VOUT -> /Battery System/3v3 rail/3v3_out :: C95(47uF), C96(47uF), R154(23.2kΩ)
  - pin 5 SW -> unconnected-(U57-SW-Pad5) :: 
  - pin 6 SW -> unconnected-(U57-SW-Pad6) :: 
  - pin 7 BOOT -> unconnected-(U57-BOOT-Pad7) :: 
  - pin 8 VCC -> Net-(U57-VCC) :: C94(1uF)
  - pin 9 FB -> Net-(U57-FB) :: R154(23.2kΩ), R155(10kΩ)
  - pin 10 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin 11 RT -> Net-(U57-RT) :: R153(20kΩ)

## U58 TPSM33625RDNR
- sheet: ../power/5vrail.kicad_sch (5v rail)
- datasheet: https://item.szlcsc.com/datasheet/TPSM33625RDNR/8040204.html
  - pin 1 PGOOD -> Power/5V-Buck/PGOOD :: R23(47Ω)
  - pin 2 EN -> Net-(Q12-D) :: Q12(L2N7002SLLT1G), R157(100kΩ)
  - pin 3 VIN -> /Battery System/3v3 rail/VCC :: C92(100nF), C93(4.7uF), C97(100nF), C98(4.7uF), C99(47uF), D4(SS36), D5(SS36), D6(SS36), D7(SS36), R157(100kΩ), ...
  - pin 4 VOUT -> /Battery System/5v rail/5V-OUT :: C101(22uF), C102(22uF), C108(100nF), C109(22uF), R11(100kΩ), R159(40.2kΩ), R169(100kΩ), U60(MT9700-N)
  - pin 5 SW -> unconnected-(U58-SW-Pad5) :: 
  - pin 6 SW -> unconnected-(U58-SW-Pad6) :: 
  - pin 7 BOOT -> unconnected-(U58-BOOT-Pad7) :: 
  - pin 8 VCC -> Net-(U58-VCC) :: C100(1uF)
  - pin 9 FB -> Net-(U58-FB) :: R159(40.2kΩ), R160(10kΩ)
  - pin 10 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin 11 RT -> Net-(U58-RT) :: R158(15.8kΩ)

## U60 MT9700-N
- sheet: ../connectors/mt9700-efuse.kicad_sch (mt9700-efuse1)
- datasheet: https://item.szlcsc.com/datasheet/MT9700-N/44491709.html
  - pin 1 VOUT -> /Battery System/mt9700-efuse1/OUT :: C110(100nF), D8(SMF5_0A_C2857263), U61(150uF)
  - pin 2 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin 3 SET -> /Battery System/mt9700-efuse1/SET :: R12(0603WAF3401T5E)
  - pin 4 EN -> Net-(U60-EN) :: R168(47Ω), R169(100kΩ), R170(4.7kΩ)
  - pin 5 VIN -> /Battery System/5v rail/5V-OUT :: C101(22uF), C102(22uF), C108(100nF), C109(22uF), R11(100kΩ), R159(40.2kΩ), R169(100kΩ), U58(TPSM33625RDNR)

## U62 PCA9685PW,118
- sheet: ../mcu/25_Microcontroller-PWM-IC.kicad_sch (PWM Driver)
- datasheet: https://www.nxp.com.cn/docs/en/data-sheet/PCA9685.pdf
  - pin 1 A0 -> Net-(U62-A0) :: R187(10kΩ)
  - pin 2 A1 -> Net-(U62-A1) :: R182(10kΩ)
  - pin 3 A2 -> Net-(U62-A2) :: R183(10kΩ)
  - pin 4 A3 -> Net-(U62-A3) :: R184(10kΩ)
  - pin 5 A4 -> Net-(U62-A4) :: R185(10kΩ)
  - pin 6 LED0 -> Net-(U62-LED0) :: R171(47Ω)
  - pin 7 LED1 -> Net-(U62-LED1) :: R172(47Ω)
  - pin 8 LED2 -> Net-(U62-LED2) :: R177(47Ω)
  - pin 9 LED3 -> Net-(U62-LED3) :: R178(47Ω)
  - pin 10 LED4 -> Net-(U62-LED4) :: R179(47Ω)
  - pin 11 LED5 -> Net-(U62-LED5) :: R180(47Ω)
  - pin 12 LED6 -> Net-(U62-LED6) :: R181(47Ω)
  - pin 13 LED7 -> unconnected-(U62-LED7-Pad13) :: 
  - pin 14 VSS -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin 15 LED8 -> unconnected-(U62-LED8-Pad15) :: 
  - pin 16 LED9 -> unconnected-(U62-LED9-Pad16) :: 
  - pin 17 LED10 -> unconnected-(U62-LED10-Pad17) :: 
  - pin 18 LED11 -> unconnected-(U62-LED11-Pad18) :: 
  - pin 19 LED12 -> unconnected-(U62-LED12-Pad19) :: 
  - pin 20 LED13 -> unconnected-(U62-LED13-Pad20) :: 
  - pin 21 LED14 -> unconnected-(U62-LED14-Pad21) :: 
  - pin 22 LED15 -> unconnected-(U62-LED15-Pad22) :: 
  - pin 23 OE# -> Net-(U62-OE#) :: R189(10kΩ)
  - pin 24 A5 -> +3V3 :: C1(10uF), C103(100nF), C104(10uF), C117(100nF), C118(1uF), C126(1uF), C127(100nF), C131(470nF), C14(100nF), C15(1uF), ...
  - pin 25 EXTCLK -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin 26 SCL -> /Battery System/PWM Driver/SCL :: U7(~), U9(~)
  - pin 27 SDA -> /Battery System/PWM Driver/SDA :: U6(~), U8(~)
  - pin 28 VDD -> +3V3 :: C1(10uF), C103(100nF), C104(10uF), C117(100nF), C118(1uF), C126(1uF), C127(100nF), C131(470nF), C14(100nF), C15(1uF), ...

## U64 BQ7694202PFBR
- sheet: ../battery/18_Battery-BMS.kicad_sch (Battery BMS Interface)
- datasheet: https://www.ti.com/cn/lit/gpn/bq76942
  - pin 1 NC -> unconnected-(U64-NC-Pad1) :: 
  - pin 2 VC9 -> /Battery System/Battery BMS Interface/VC3 :: C111(220nF), C112(220nF), R174(20Ω)
  - pin 3 NC -> unconnected-(U64-NC-Pad3) :: 
  - pin 4 VC8 -> /Battery System/Battery BMS Interface/VC3 :: C111(220nF), C112(220nF), R174(20Ω)
  - pin 5 NC -> unconnected-(U64-NC-Pad5) :: 
  - pin 6 VC7 -> /Battery System/Battery BMS Interface/VC3 :: C111(220nF), C112(220nF), R174(20Ω)
  - pin 7 NC -> unconnected-(U64-NC-Pad7) :: 
  - pin 8 VC6 -> /Battery System/Battery BMS Interface/VC3 :: C111(220nF), C112(220nF), R174(20Ω)
  - pin 9 NC -> unconnected-(U64-NC-Pad9) :: 
  - pin 10 VC5 -> /Battery System/Battery BMS Interface/VC3 :: C111(220nF), C112(220nF), R174(20Ω)
  - pin 11 NC -> unconnected-(U64-NC-Pad11) :: 
  - pin 12 VC4 -> /Battery System/Battery BMS Interface/VC3 :: C111(220nF), C112(220nF), R174(20Ω)
  - pin 13 VC3 -> /Battery System/Battery BMS Interface/VC3 :: C111(220nF), C112(220nF), R174(20Ω)
  - pin 14 VC2 -> /Battery System/Battery BMS Interface/VC3 :: C111(220nF), C112(220nF), R174(20Ω)
  - pin 15 VC1 -> /Battery System/Battery BMS Interface/VC1 :: C112(220nF), C114(220nF), R175(20Ω)
  - pin 16 VC0 -> /Battery System/Battery BMS Interface/VC0 :: C113(220nF), D25(MMSZ4685T1G), D26(BAT46W-7-F), R176(20Ω)
  - pin 17 VSS -> VSS :: C113(220nF), C114(220nF), C120(1uF), C121(100pF), C130(1uF), C132(1uF), C134(100nF), C32(2.2uF), D25(MMSZ4685T1G), D26(BAT46W-7-F), ...
  - pin 18 SRP -> Net-(U64-SRP) :: C115(100nF), C116(100pF), R186(100Ω)
  - pin 19 NC -> unconnected-(U64-NC-Pad19) :: 
  - pin 20 SRN -> Net-(U64-SRN) :: C115(100nF), C116(100pF), R188(100Ω)
  - pin 21 TS1 -> /Battery System/Battery BMS Interface/TS1 :: 
  - pin 22 TS2 -> /Battery System/Battery BMS Interface/TS2 :: R217(5.1kΩ)
  - pin 23 TS3 -> /Battery System/Battery BMS Interface/TS3 :: 
  - pin 24 REG18 -> /Battery System/Battery BMS Interface/REG18 :: C32(2.2uF), R120(4.7k)
  - pin 25 ALERT -> BQ/ALERT :: R19(47Ω), R196(10kΩ)
  - pin 26 SCL -> SCL_SLOW :: R51(4.7kΩ), U13(~), U17(~), U3(~), U30(MCP4725A0T-E/CH), U31(ADS1115IDGST), U56(INA226AIDGSR), U56(INA226AIDGSR), U65(INA226AIDGSR), U65(INA226AIDGSR), ...
  - pin 27 SDA -> SDA_SLOW :: R52(4.7kΩ), U12(~), U16(~), U2(~), U30(MCP4725A0T-E/CH), U31(ADS1115IDGST), U56(INA226AIDGSR), U56(INA226AIDGSR), U6(~), U65(INA226AIDGSR), ...
  - pin 28 HDQ -> unconnected-(U64-HDQ-Pad28) :: 
  - pin 29 CFETOFF -> unconnected-(U64-CFETOFF-Pad29) :: 
  - pin 30 DFETOFF -> unconnected-(U64-DFETOFF-Pad30) :: 
  - pin 31 DCHG -> unconnected-(U64-DCHG-Pad31) :: 
  - pin 32 DDSG -> unconnected-(U64-DDSG-Pad32) :: 
  - pin 33 RST_SHUT -> BQ/RST-SHUT :: R193(100kΩ), R20(47Ω)
  - pin 34 REG2 -> Net-(U64-REG1) :: R192(82kΩ)
  - pin 35 REG1 -> Net-(U64-REG1) :: R192(82kΩ)
  - pin 36 REGIN -> VSS :: C113(220nF), C114(220nF), C120(1uF), C121(100pF), C130(1uF), C132(1uF), C134(100nF), C32(2.2uF), D25(MMSZ4685T1G), D26(BAT46W-7-F), ...
  - pin 37 BREG -> VSS :: C113(220nF), C114(220nF), C120(1uF), C121(100pF), C130(1uF), C132(1uF), C134(100nF), C32(2.2uF), D25(MMSZ4685T1G), D26(BAT46W-7-F), ...
  - pin 38 FUSE -> unconnected-(U64-FUSE-Pad38) :: 
  - pin 39 PDSG -> /Battery System/Battery BMS Interface/PDSG :: 
  - pin 40 PCHG -> /Battery System/Battery BMS Interface/PCHG :: D30(MMSZ5267BT1G), R202(68kΩ)
  - pin 41 LD -> Net-(U64-LD) :: R195(10kΩ)
  - pin 42 PACK -> Net-(U64-PACK) :: R194(10kΩ)
  - pin 43 DSG -> /Battery System/Battery BMS Interface/DSG :: R198(100Ω)
  - pin 44 NC -> unconnected-(U64-NC-Pad44) :: 
  - pin 45 CHG -> /Battery System/Battery BMS Interface/CHG :: R197(100Ω)
  - pin 46 CP1 -> Net-(U64-CP1) :: C119(470nF)
  - pin 47 BAT -> Net-(U64-BAT) :: C119(470nF), C120(1uF), C121(100pF), R190(100Ω), R191(100Ω)
  - pin 48 VC10 -> /Battery System/Battery BMS Interface/VC4 :: C111(220nF), R173(20Ω)

## U65 INA226AIDGSR
- sheet: ../connectors/INA226_SINGLE_CURR_SENSOR.kicad_sch (INA226_SINGLE_CURR_SENSOR_SERVO)
- datasheet: https://item.szlcsc.com/datasheet/INA226AIDGSR/50860.html
  - pin 1 A1 -> SCL_SLOW :: R51(4.7kΩ), U13(~), U17(~), U3(~), U30(MCP4725A0T-E/CH), U31(ADS1115IDGST), U56(INA226AIDGSR), U56(INA226AIDGSR), U64(BQ7694202PFBR), U67(X1270WV-2X08B-6TV01), ...
  - pin 2 A0 -> SCL_SLOW :: R51(4.7kΩ), U13(~), U17(~), U3(~), U30(MCP4725A0T-E/CH), U31(ADS1115IDGST), U56(INA226AIDGSR), U56(INA226AIDGSR), U64(BQ7694202PFBR), U67(X1270WV-2X08B-6TV01), ...
  - pin 3 Alert -> Current/INA226-SERVO-0x4F/ALERT :: R44(47Ω)
  - pin 4 SDA -> SDA_SLOW :: R52(4.7kΩ), U12(~), U16(~), U2(~), U30(MCP4725A0T-E/CH), U31(ADS1115IDGST), U56(INA226AIDGSR), U56(INA226AIDGSR), U6(~), U64(BQ7694202PFBR), ...
  - pin 5 SCL -> SCL_SLOW :: R51(4.7kΩ), U13(~), U17(~), U3(~), U30(MCP4725A0T-E/CH), U31(ADS1115IDGST), U56(INA226AIDGSR), U56(INA226AIDGSR), U64(BQ7694202PFBR), U67(X1270WV-2X08B-6TV01), ...
  - pin 6 VS+ -> +3V3 :: C1(10uF), C103(100nF), C104(10uF), C117(100nF), C118(1uF), C126(1uF), C127(100nF), C131(470nF), C14(100nF), C15(1uF), ...
  - pin 7 GND -> GND :: C100(1uF), C101(22uF), C102(22uF), C103(100nF), C104(10uF), C108(100nF), C109(22uF), C110(100nF), C117(100nF), C118(1uF), ...
  - pin 8 VBUS -> /Battery System/INA226_SINGLE_CURR_SENSOR_SERVO/VIN_P :: 
  - pin 9 VIN- -> /Battery System/INA226_SINGLE_CURR_SENSOR_SERVO/VIN_N :: 
  - pin 10 VIN+ -> /Battery System/INA226_SINGLE_CURR_SENSOR_SERVO/VIN_P :: 

## U66 NCP718ASN330T1G
- sheet: bms_button_logic.kicad_sch (bms_button_logic)
- datasheet: https://atta.szlcsc.com/upload/public/pdf/source/20210813/8C1C10F20D6048507834084705E93F3A.pdf
  - pin 1 IN -> Net-(U66-IN) :: C130(1uF), F5(JK-nSMD050-30)
  - pin 2 GND -> VSS :: C113(220nF), C114(220nF), C120(1uF), C121(100pF), C130(1uF), C132(1uF), C134(100nF), C32(2.2uF), D25(MMSZ4685T1G), D26(BAT46W-7-F), ...
  - pin 3 EM -> Net-(U66-EM) :: R120(4.7k), R215(100kΩ)
  - pin 4 NC/ADJ -> unconnected-(U66-NC/ADJ-Pad4) :: 
  - pin 5 OUT -> /Battery System/Battery BMS Interface/ALERT_PULLUP :: C132(1uF), R196(10kΩ), U68(PMEG10030ELPX)

