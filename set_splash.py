#!bin/env python3
import os
import sys
import struct
import re
from wand.image import Image

CURRENT_FILE = os.path.dirname(__file__)

BMP3_FORMAT = "<HIHHIIiiHHIIIIII"
BMP3_HEADER_SIZE = 54
BI_RGB = 0


def bmp3_struct_to_dict(bmp3_header_raw):
    vals = struct.unpack(BMP3_FORMAT, bmp3_header_raw)
    return dict(
        # Bitmap file header
        type=vals[0],
        img_size=vals[1],
        reserved1=vals[2],
        reserved2=vals[3],
        data_offset=vals[4],
        # DIB header
        dib_size=vals[5],
        img_width=vals[6],
        img_height=vals[7],
        n_color_planes=vals[8],
        img_depth=vals[9],
        compression=vals[10],
        data_size=vals[11],
        resolution_x=vals[12],
        resolution_y=vals[13],
        n_colors=vals[14],
        n_important_colors=vals[15]
    )


def bmp3_dict_to_struct(bmp3_header_dict):
    return struct.pack(BMP3_FORMAT, *bmp3_header_dict.values())


def main(argc, argv):
    if argc < 1:
        print("Please provide path to image, i.e, run script as: python insert_splash.py path_to_image")
        return 1

    splash_image_path = os.path.abspath(argv[0])
    boot_img_path = os.path.join(CURRENT_FILE, "tmp/firmware_update/Image/boot.img")

    # Read boot.img
    try:
        with open(boot_img_path, "rb") as boot_img:
            byte_stream = boot_img.read()
    except FileNotFoundError:
        print("Error: Unable to open boot.img; ensure the update image has been downloaded and unpacked.")
        return 1

    # Find the magic BMP3 sequence
    bmp3_header_re = re.compile(b"\x42\x4d.{12}[\x28]\x00", re.DOTALL)
    bmp3_iter = bmp3_header_re.finditer(byte_stream)
    for bmp3 in bmp3_iter:
        img_offset = bmp3.start()
        bmp3_header_raw = byte_stream[img_offset:img_offset+BMP3_HEADER_SIZE]
        bmp3_header = bmp3_struct_to_dict(bmp3_header_raw)

        # Only replace image if the bitmap is uncompressed BI RGB
        if bmp3_header["compression"] != BI_RGB:
            print("Bitmap is not BI RGB; skipping")
            continue

        # Read the desired splash image from disk
        splash_image = Image(filename=splash_image_path)

        # Display expects image to be flipped
        splash_image.rotate(180)

        # Resize image to display size
        splash_image.resize(
            abs(bmp3_header["img_width"]), abs(bmp3_header["img_height"])
        )

        # Force 24 depth bit map
        splash_image.type = "truecolor"
        # Remove alpha channel and fill with background color
        splash_image.background_color = "white"
        splash_image.alpha_channel = "remove"
        # Convert to BMP3 format
        splash_bmp = splash_image.convert("BMP3")
        # Grab the new image
        splash_image_raw = splash_bmp.make_blob()

        # Perform size safety check
        img_size = len(splash_image_raw)
        if img_size != bmp3_header["img_size"]:
            print("Error: Splash image size does not match the expected size")
            return 1

        # Insert data to byte stream
        byte_stream = bytearray(byte_stream)
        byte_stream[img_offset:img_offset + img_size] = splash_image_raw

        # Write new boot.img
        with open(boot_img_path, "bw") as boot_img:
            boot_img.write(bytes(byte_stream))

    return 0


if __name__ == "__main__":
    ret_code = main(len(sys.argv[1:]), sys.argv[1:])
    sys.exit(ret_code)
