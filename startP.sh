#!/bin/sh
git add .
git commit -m "auto commit2"
git push origin master
echo "Publishing display"
pass=$1
host='pi@192.168.1.205'
sshpass -p $pass ssh $host "pkill -f python"
sshpass -p $pass ssh $host  "cd thermostatProject;git pull origin master"
sshpass -p $pass ssh $host "export DISPLAY=:0;python3 thermostatProject/thermostatStart.py"