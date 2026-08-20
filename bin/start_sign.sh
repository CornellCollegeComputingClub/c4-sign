#!/bin/bash

set -o errexit
#set -x

cd /home/c4/c4-sign

sudo /home/c4/c4-sign/venv/bin/python3 /home/c4/c4-sign/bin/message.py "NETWORK" "TARGET" > /dev/null

while [["$(systemctl is-active network.target)" != 'active']]
do
    echo 'Waiting for network.'
    sleep '0.2'
done

sudo /home/c4/c4-sign/venv/bin/python3 /home/c4/c4-sign/bin/message.py "INTERNET" "CHECK" > /dev/null

# do we have internet?
function checkInternet {
    curl -s --head  --request GET https://www.google.com | grep "200" > /dev/null
}

# wait for internet
while ! checkInternet; do
    sleep 5
done

sudo /home/c4/c4-sign/venv/bin/python3 /home/c4/c4-sign/bin/message.py "GIT" "PULL" > /dev/null

git pull

# sudo python3 -m pip install -e .
# this takes a while to run. TODO: FIX.

sudo /home/c4/c4-sign/venv/bin/python3 /home/c4/c4-sign/bin/message.py "JAVA" "COMPILE" > /dev/null

/home/c4/c4-sign/venv/bin/python3 tools/compile_java_project.py

sudo /home/c4/c4-sign/venv/bin/python3 /home/c4/c4-sign/bin/message.py "STARTING" "SIGN" > /dev/null

sudo /home/c4/c4-sign/venv/bin/python3 -m c4_sign

exit 0
