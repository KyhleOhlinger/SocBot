sudo apt update -y
sudo apt install python2 -y
sudo apt-get remove python3-pip -y; sudo apt-get install python3-pip -y

## Install Get-Pip
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
sudo python2 get-pip.py

## Install Prerequisits
sudo apt-get install -y --no-install-recommends python-pip python2.7-dev python3-dev ssdeep libfuzzy-dev libfuzzy2 libimage-exiftool-perl libmagic1 build-essential git libssl-dev
sudo pip2 install -U pip setuptools && sudo pip3 install -U pip setuptools

## Install Analyzers and Responders

cd /opt
git clone https://github.com/TheHive-Project/Cortex-Analyzers
for I in $(find Cortex-Analyzers -name 'requirements.txt'); do sudo -H pip2 install -r $I; done && \
for I in $(find Cortex-Analyzers -name 'requirements.txt'); do sudo -H pip3 install -r $I || true; done