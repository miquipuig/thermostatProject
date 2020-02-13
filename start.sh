#!/bin/bash
export DISPLAY=:0
xinit
# xinit /bin/sh -c 'exec python3 thermostatProject/thermostatStart.py' &
python3 thermostatProject/thermostatStart.py &
xset q
xset -dpms
xset s noblank
xset s off 
