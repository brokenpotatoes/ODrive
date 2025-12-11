## Important Note
This REPO is unaffiliated with ODrive. Do NOT contact ODrive with any issues.

This is a mod of the original ODrive fw v0.5.6 to run on MKS XDRIVE MINI. The MKS ships with extremely buggy 0.5.1 firmware and is effectively unusable without a firmware update.

CHANGES:
- Removed axis1
- Bypassed OTP validation
TO DO:
- Add the possibility to build firmware for original ODrives from this fork
- Instead of bypassing the OTP flash a valid OTP to the MKS

## Overview

This project is all about accurately driving brushless motors, for cheap. The aim is to make it possible to use inexpensive brushless motors in high performance robotics projects, like [this](https://www.youtube.com/watch?v=WT4E5nb3KtY).

[![pip install odrive (nightly)](https://github.com/madcowswe/ODrive/workflows/pip%20install%20odrive%20(nightly)/badge.svg)](https://github.com/madcowswe/ODrive/actions?query=workflow%3A%22pip+install+odrive+%28nightly%29%22)

Please refer to the [Developer Guide](https://docs.odriverobotics.com/v/latest/developer-guide.html#) to get started with ODrive firmware development.


### Repository Structure
 * **Firmware**: ODrive firmware
 * **tools**: Python library & tools
 * **docs**: Documentation

### Other Resources

 * [Main Website](https://www.odriverobotics.com/)
 * [User Guide](https://docs.odriverobotics.com/)
 * [Forum](https://discourse.odriverobotics.com/)
 * [Chat](https://discourse.odriverobotics.com/t/come-chat-with-us/281)
