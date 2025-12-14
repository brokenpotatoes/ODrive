# Building the firmware

This page covers the common build steps for the firmware in this repository.

Prerequisites (Linux example)

- Python 3.8+
- `pip`
- `gcc-arm-none-eabi`
- `openocd` (for ST-Link flash targets)
- `stlink-tools` (optional)
- `tup` (the Makefile uses `tup` during the build)
- `make`

Install common packages on Debian/Ubuntu:

```bash
sudo apt update
sudo apt install -y python3 python3-pip make gcc-arm-none-eabi openocd stlink-tools tup
```

Build steps

```bash
cd Firmware
make
# or parallel: make -j$(nproc)
```

After a successful build, firmware artifacts live in `Firmware/build/` (for example `ODriveFirmware.hex` and `ODriveFirmware.elf`).

Flash using ST-Link / OpenOCD

```bash
cd Firmware
make flash    # uses openocd & stlink (flash-stlink2 target)
```

Other targets in the `Firmware/Makefile` include: `clean`, `flash-bmp`, `dfu`, `erase`, `unlock`, and `libfibre-*` build helpers.

Notes

- The Makefile will call `tup` — ensure `tup` is installed and configured.
- Building the Python tools (odrivetool) is done in the `tools` folder. Install with `pip install -e tools` for local development.
