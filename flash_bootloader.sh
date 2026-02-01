#!/bin/env bash

# Abort script if any command fails
set -e

# Read boot offset from parameter.txt
BOOT_OFFSET=0x$(cat tmp/firmware_update/parameter.txt | grep CMDLINE | awk -F "," '{for (i=1;i<NF;i++) if($i~/\(boot\)/) print $i}' | cut -d@ -f2 | sed -n "s/0x0*\(.*\)(boot)/\1/p")

# Upload bootloader
sudo rkdeveloptool db ./tmp/firmware_update/MiniLoaderAll.bin

# Add a small delay before uploading the boot image
sleep 1

# Upload boot.img
sudo rkdeveloptool wl $BOOT_OFFSET ./tmp/firmware_update/Image/boot.img

# Add a small delay before rebooting
sleep 1

# Reboot printer
sudo rkdeveloptool reboot
