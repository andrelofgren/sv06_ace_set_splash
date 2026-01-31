# sv06_ace_set_splash
This program consists of some small scripts that let you insert a custom splash screen into the official SOVOL SV06 (PLUS) ACE firmware.
Running this program is carried out in six steps, namely:

1) Installing dependencies: ```bash sudo apt install git python3-venv imagemagick```
2) Downloading the image for your printer: ```bash ./download-update-img.sh```
3) Unpacking the image: ```bash ./unpack-update-img.sh path-to-update-image```
4) Replacing the splash screen in boot.img:```bash ./set_splash.sh path-to-splash-image```
5) Repacking the image: ```bash ./pack-update-img.sh```
6) Flashing the firmware

For instructions on how to flash the firmware https://wiki.sovol3d.com/en/SV06-ACE-image-flashing-tutorial if you have access to a Windows computer. If on Linux, follow instructions at https://forum.sovol3d.com/t/linux-board-flashing-tool-for-sv06-ace/8076/3.

Also, depending on your system there might be other dependencies than the one listed.

## WARNING
Flashing always carries the risk of bricking your device, and will most likely void you of you warranty. Ensure you have read through the program thoroughly before running and flashing as I take zero responsibility for what these scripts might do to your system. Also, be aware that flashing the resulting image will completely wipe your printer, so make sure you back up anything of value before flashing.
