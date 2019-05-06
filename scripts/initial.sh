#!/usr/bin/env bash
source env/bin/activate
scp berater/secret.py suun@weixinbak.njunova.com:~/
ssh suun@weixinbak.njunova.com "
rm -rf berater;
git clone https://github.com/inhzus/berater;
cd berater;
mv ~/secret.py berater/;
sudo apt-get install virtualenv;
virtualenv env -p python3;
source env/bin/activate;
pip3 install -r requirements.txt;
"
