# DFU Flashing using STM32CubeProgrammer

This page explains how to flash a released firmware image using the STM32CubeProgrammer and the board bootloader.

1) Download the firmware from Releases

- Visit: https://github.com/brokenpotatoes/ODrive/releases
- Download the latest firmware artifact (for example `ODriveFirmware.hex` or `ODriveFirmware.bin`).

2) Prepare the board for the system bootloader (USB DFU)

- Connect the board to your PC via USB.
- Hold the `BOOT` button, then press and release `RESET` while still holding `BOOT`. Release `BOOT` after reset. The MCU will enter the system bootloader.

3) Open STM32CubeProgrammer

- Launch STM32CubeProgrammer (Windows/macOS/Linux) and select the `USB` interface (or `ST-LINK` if you prefer flashing via ST-Link).
- If using USB DFU, STM32CubeProgrammer should detect the device in the list once the board is in bootloader mode.

4) Flash the firmware

- In STM32CubeProgrammer choose `Erasing & Programming` (or `Download`), then `Browse` to select the downloaded `.hex` or `.bin` file.
- Select the target memory address if required (use the default for `.hex` files). Click `Start` or `Download`.
- Wait for the operation to complete and verify there are no errors.

5) Restart the board

- After flashing, disconnect and power-cycle the board (or press `RESET`) to boot the new firmware.

Notes and troubleshooting

- If STM32CubeProgrammer does not detect the device, ensure the USB cable supports data and try another USB port.
- On Linux you may need udev rules or run STM32CubeProgrammer as `sudo` to access USB devices.
- As a fallback you can use `ST-LINK` flashing (`make flash` / `openocd`) if you have an ST-Link programmer.
