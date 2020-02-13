#!/bin/bash
sudo apt-get install fontconfig
sudo cp -R thermoFonts /usr/share/fonts

sudo apt-get install python3-pip

pip3 install virtualenv
python3 -c "import sys; print(sys.path)"
sudo rm -r venv
virtualenv venv
source venv/bin/activate