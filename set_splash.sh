#!/bin/env bash

# Abort script if any command fails
set -e

# Read splash image path
SPLASH_IMG_PATH=$1

if [[ ! $SPLASH_IMG_PATH ]]; then
    echo "Please provide path to splash image, i.e runscript as: ./insert_splash.sh path_to_splash_image"
    exit 1
fi

# Set environment variables
PYVENV_DIR=$(pwd)/tmp/pydeps

# Create temporary directory
mkdir -p tmp

# Create a python environment for image magick
python3 -m venv $PYVENV_DIR
$PYVENV_DIR/bin/pip install wand

# Set splash image
$PYVENV_DIR/bin/python3 set_splash.py $SPLASH_IMG_PATH

echo "Splash image '$SPLASH_IMG_PATH' was successfully inserted!"
