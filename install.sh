#!/bin/bash
echo 'hola'
sudo apt-get install fontconfig
sudo cp -R thermoFonts /usr/share/fonts
sudo apt-get install build-essential python-dev python-setuptools python-pip python-smbus -y
sudo apt-get install python3-pip
sudo apt-get install python3-tk

sudo apt-get install libopenjp2-7
sudo apt-install libtiff5
sudo apt-get install libatlas-base-dev
sudo apt install python3-venv
pip3 install virtualenv
python3 -c "import sys; print(sys.path)"
sudo rm -r venv
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
sudo apt-get install python3-tk