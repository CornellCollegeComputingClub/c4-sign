sudo apt update
sudo apt install -y python3-pip git python3-dev python3-libgpiod ffmpeg maven
git clone https://github.com/CornellCollegeComputingClub/c4-sign
cd c4-sign
git config pull.rebase false
sudo -H python3 -m venv ./venv
sudo -H /home/c4/c4-sign/venv/bin/python3 -m pip install -e '.[physical]'
sudo cp -v ./bin/c4-sign.service /lib/systemd/system/
sudo systemctl enable c4-sign.service
sudo reboot now
