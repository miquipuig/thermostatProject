#!/bin/sh
echo "Publishing display"
pass=$1
host='pi@192.168.1.205'
sshpass -p $pass ssh $host "pkill -f python"
sshpass -p $pass scp -r  * $host:thermostat/
VAREXE=thermostat/thermostatStart.py
sshpass -p $pass ssh $host "export DISPLAY=:0; xinit /bin/sh -c 'exec python3 thermostat/thermostatStart.py' --"