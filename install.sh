sudo apt install -y python3-pip git
git clone https://github.com/CornellCollegeComputingClub/c4-sign
cd c4-sign
git config pull.rebase false
sudo ./rgbmatrixinstall.sh
sudo -H python3 -m pip install -e ~/c4-sign
sudo cp -v ./bin/c4-sign.service /lib/systemd/system/
sudo systemctl enable c4-sign.service
sudo reboot now
