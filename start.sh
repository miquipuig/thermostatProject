export DISPLAY=:0
# xset -dpms
# xset s noblank
# xset s off 
xinit /bin/sh -c 'exec python3 thermostatProject/thermostatStart.py' &
