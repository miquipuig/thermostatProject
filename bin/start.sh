#!/bin/bash
APP_ROOT="$(dirname "$(dirname "$(readlink -fm "$0")")")"

export DISPLAY=:0
xinit
# xinit /bin/sh -c 'exec python3 thermostatProject/thermostatStart.py' &
cd $APP_ROOT
PACKAGE="heatPicontrol"

python3 -m $PACKAGE &
xset q
xset -dpms
xset s noblank
xset s off 
