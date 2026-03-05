# I2C Rail Audit (`SCL_SLOW` / `SDA_SLOW`)

Generated on `2026-03-05` from:
- Schematic: `hardware/kicad/svea_powerboard_rev3.kicad_sch`
- Fresh netlist: `build/kicad/quality/netlist_i2c_audit.xml`

All addresses below are **7-bit I2C addresses unless explicitly noted otherwise**.

## Scope and method
1. Exported a fresh netlist with `kicad-cli sch export netlist`.
2. Enumerated every node on `SCL_SLOW` and `SDA_SLOW`.
3. Derived addresses from **actual pin straps + datasheet address tables**.
4. Did not trust symbol comments/labels as source of truth.

## Rail summary
| Rail | Pull-up | Net notes |
|---|---|---|
| `SCL_SLOW` | `R105 = 2.2k` to `+3V3` | Connected to all on-bus devices, `U83` connector pin 10, and `JP2001` pin 1 |
| `SDA_SLOW` | `R118 = 2.2k` to `+3V3` | Connected to all on-bus devices, `U83` connector pin 12, and `JP2002` pin 1 |

## I2C device matrix (address + speed)
| Ref | Device | Bus state on this board | Address (7-bit) | Supported I2C frequency (datasheet) | Strap / decode evidence |
|---|---|---|---|---|---|
| `CUR_1` | `INA3221AIRGVR` | Active on `SCL_SLOW/SDA_SLOW` | `0x40` | Fast + HS: up to `2.44 MHz` | `A0` via `R98` to `GND`; INA3221 address table (`A0=GND`) |
| `CUR_2` | `INA3221AIRGVR` | Active on `SCL_SLOW/SDA_SLOW` | `0x41` | Fast + HS: up to `2.44 MHz` | `A0` via `R162` to `+3V3`; INA3221 address table (`A0=VS`) |
| `U304` | `PCAL6524HEAZ` | Active on `SCL_SLOW/SDA_SLOW` | `0x23` | Fm+: up to `1 MHz` | `ADDR` via `R19` to `+3V3`; datasheet Table 4 gives `0x46/0x47` (8-bit) |
| `U3404` | `PCAL6524HEAZ` | Active on `SCL_SLOW/SDA_SLOW` | `0x22` | Fm+: up to `1 MHz` | `ADDR` via `R243` to `GND`; datasheet Table 4 gives `0x44/0x45` (8-bit) |
| `U44` | `MCP4725A0T-E/CH` | Active on `SCL_SLOW/SDA_SLOW` | `0x60` | Standard/Fast/HS: up to `3.4 MHz` | `A0` pin to `GND`; `A2/A1=00` option for A0 variant |
| `U601` | `TPL0401B-10DCKR` | Active on `SCL_SLOW/SDA_SLOW` | `0x3E` | Standard/Fast: up to `400 kHz` | TPL0401B bit address table (`0111110b`) |
| `U72` | `INA226AIDGSR` | Active on `SCL_SLOW/SDA_SLOW` | `0x4E` | Fast + HS: up to `2.94 MHz` | `A1=SCL`, `A0=SDA` |
| `U78` | `PCA9685PW,118` | Active on `SCL_SLOW/SDA_SLOW` | `0x61` | Fm+: up to `1 MHz` | `A5=1`, `A0=1` via `R186`, `A4..A1=0` via `R184,R183,R182,R181` |
| `U80` | `BQ7694202PFBR` | Active on `SCL_SLOW/SDA_SLOW` | `0x08` (default) | `100/400 kHz` | Datasheet default I2C target bytes `0x10/0x11` (8-bit) |
| `U81` | `INA226AIDGSR` | Active on `SCL_SLOW/SDA_SLOW` | `0x4F` | Fast + HS: up to `2.94 MHz` | `A1=SCL`, `A0=SCL` |
| `U1` | `LSM6DSOXTR` | Active on `SCL_SLOW/SDA_SLOW` | `0x6B` | Standard/Fast: up to `400 kHz` | `SA0` tied high (`SDO/SA0=+3V3`) |
| `U104` | `ADS1115IRUGT` | Active on `SCL_SLOW/SDA_SLOW` | `0x49` | Standard/Fast/HS: up to `3.4 MHz` | `ADDR=+3V3` |
| `U65` | `HUSB238A-BB001-QN16R` | **Isolated by default** (`JP2001`,`JP2002` open) | Conditional: datasheet notation is `62H` (`ADDR=VDD`) or `42H` (`ADDR=GND`); if those are 8-bit transfer bytes, equivalent 7-bit addresses are `0x31` / `0x21`; floating `ADDR` => GPIO mode (no I2C address) | Fast mode: up to `400 kHz` | `ADDR/ORIENT` is not hard-strapped to VDD/GND in this design: `U65.ADDR` -> `R2007` -> `USB-C/I2C/EN` -> `U302` -> `U304` |

`U83` is a direct bus connector endpoint (`SCL_SLOW/SDA_SLOW`) and can add external I2C devices/addresses.

## Findings that matter before ordering
1. No on-board 7-bit address collisions were found on `SCL_SLOW/SDA_SLOW` in this revision.
2. **PCAL6524 address format trap:** datasheet table is shown in 8-bit transfer form (`0x44/0x45`, `0x46/0x47`). Typical firmware APIs want 7-bit (`0x22`, `0x23`).
3. `U83` exposes the same rail externally, so any plugged module can still create address conflicts.
4. `U65` only has a valid I2C address if `ADDR/ORIENT` is forced high or low during initialization; if it is floating at init, the part enters GPIO mode.

## Same-bus compatibility check
1. **Clock-rate compatibility:** all active devices are compatible at `<= 400 kHz`; do not run this shared bus above `400 kHz` because `U601`, `U1`, and `U80` top out at fast/400 kHz.
2. **Mixed fast/HS parts are fine** as long as the controller keeps the bus at the common safe rate (`100 kHz` or `400 kHz`).
3. **Protocol behavior to account for in firmware:**
   - `U78` (`PCA9685`) has default All-Call behavior (address group behavior exists in addition to its normal target address).
   - `U104` (`ADS1115`) supports SMBus/general-call features.
   - `CUR_1/CUR_2/U72/U81` (`INA3221`/`INA226`) include SMBus-style timeout behavior.
   - `U80` (`BQ76942`) can require/expect settings such as speed/CRC mode depending on configuration.
4. **Pull-up / loading margin:** bus pull-ups are `2.2k` to `3.3V` (`~1.5 mA` sink current when line is LOW). This is generally fine for on-board population, but external modules on `U83` may add parallel pull-ups and increase sink-current/rise-time stress.
5. **If enabling `U65` onto this bus:** it is still frequency-compatible (`400 kHz` fast mode), but ensure `ADDR/ORIENT` is deterministically forced HIGH or LOW at init; floating means GPIO mode and no valid I2C target address.

## Recommended pre-order checks
1. Keep firmware-side addresses in 7-bit form (especially `PCAL6524` and `BQ76942`, where many docs show 8-bit transfer bytes).
2. If you plan to use the `U83` external connector, reserve/document external module addresses before assembly.

## Datasheet references used
All datasheets used for this audit are in `hardware/kicad/datasheets/`:
- `INA3221AIRGVR_TI.pdf`
- `INA226AIDGSR_TI.pdf`
- `ADS1115IDGST_TI.pdf`
- `PCAL6524DS_NXP.pdf`
- `PCA9685PW_118_NXP.pdf`
- `TPL0401B-10-Q1_TI.pdf`
- `BQ7694202PFBR_TI.pdf`
- `LSM6DSOX_C481766.pdf`
- `MCP4725A0T-E-CH_MICROCHIP.pdf`
- `HUSB238A-BB001-QN16R.pdf` (checked for the optional jumper-isolated path)
