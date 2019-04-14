#!/usr/bin/env bash
source env/Scripts/activate
pip3 freeze > req.txt
scp berater/secret.py req.txt suun@weixinbak.njunova.com:~/
rm req.txt
ssh suun@weixinbak.njunova.com "
rm -rf berater;
git clone https://github.com/inhzus/berater;
cd berater;
mv ~/secret.py berater/;
sudo apt-get install virtualenv;
virtualenv env -p python3;
source env/bin/activate;
pip3 install -r ~/req.txt;
rm ~/req.txt;
"
