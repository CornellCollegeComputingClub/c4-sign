sudo apt install -y python3-pip git python3-dev python3-libgpiod
sudo pip3 install --upgrade adafruit-python-shell click
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/libgpiod.py
sudo python3 libgpiod.py
git clone https://github.com/CornellCollegeComputingClub/c4-sign
cd c4-sign
git config pull.rebase false
sudo -H python3 -m pip install -e '.[physical]'
sudo cp -v ./bin/c4-sign.service /lib/systemd/system/
sudo systemctl enable c4-sign.service
sudo reboot now
