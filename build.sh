#!/bin/bash

echo "Building CableDrop executable..."

# Create dist directory
mkdir -p dist

# Build with PyInstaller
python3 -m PyInstaller \
  --onefile \
  --windowed \
  --add-data "Home.html:." \
  --add-data "Home.js:." \
  --add-data "Home.css:." \
  --name CableDrop \
  app.py

echo "Build complete! Executable is in dist/CableDrop"
