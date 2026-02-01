# sv06_ace_set_splash
This program consists of scripts that let you insert a custom splash screen into the official SOVOL SV06 (PLUS) ACE firmware.
Running this program is carried out in five steps, namely:

1) Installing dependencies: ```./install_deps_debian.sh```
2) Downloading the image for your printer: ```./download-update-img.sh```
3) Unpacking the image: ```./unpack-update-img.sh path-to-update-image```
4) Replacing the splash screen in boot.img:```./set_splash.sh path-to-splash-image```
5) Boot printer into maskrom and then run ```./flash_bootloader.sh``` to flash new boot.img

For instructions on how to boot into maskrom see the official flashing tutorial for SV06 ACE printers: https://wiki.sovol3d.com/en/SV06-ACE-image-flashing-tutorial. Also, depending on your system there might be other dependencies than the ones listed.

## WARNING
Flashing always carries the risk of bricking your device, and will most likely void you of your warranty. Ensure you have read through the program thoroughly before running and flashing as I take zero responsibility for what these scripts might do to your system. Also, be aware that flashing the resulting image will completely wipe your printer, so make sure you back up anything of value before flashing.
