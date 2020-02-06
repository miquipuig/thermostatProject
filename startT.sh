#!/bin/sh
echo "Publishing display"
pass=$1
host='pi@192.168.1.205'
sshpass -p $pass ssh $host "pkill -f python"
sshpass -p $pass scp -r  * $host:thermostatProject/
sshpass -p $pass ssh $host "export DISPLAY=:0;python3 thermostatProject/thermostatStart.py"