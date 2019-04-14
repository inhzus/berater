#!/usr/bin/env bash
source env/Scripts/activate
pip3 freeze > req.txt
scp berater/secret.py req.txt suun@weixinbak.njunova.com:~/berater/berater
rm req.txt
ssh suun@weixinbak.njunova.com "
cd ~/berater;
source env/bin/activate;
git checkout -- .;
git pull;
pip3 install -r berater/req.txt;
rm berater/req.txt;
"
