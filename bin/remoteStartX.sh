#!/bin/sh
echo "Publishing display"
pass=$1
host='pi@192.168.1.205'
sshpass -p $pass ssh $host "pkill -f python"
sshpass -p $pass ssh $host "export DISPLAY=:0; xinit"


# Redirect stdout to one file and stderr to another file:

# command > out 2>error
# Redirect stdout to a file (>out), and then redirect stderr to stdout (2>&1):

# command >out 2>&1
# Redirect both to a file (this isn't supported by all shells, bash and zsh support it, for example, but sh and ksh do not):

# command &> out