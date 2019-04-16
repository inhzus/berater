#!/usr/bin/env bash
source env/Scripts/activate
pip3 freeze > req.txt
scp berater/secret.py req.txt suun@weixinbak.njunova.com:~/
rm req.txt
ssh suun@weixinbak.njunova.com "
cd ~/berater;
source env/bin/activate;
git fetch;
git reset origin/master --hard;
git clean -df;
mv ~/secret.py berater/secret.py;
pip3 install -r ~/req.txt;
rm ~/req.txt;
"
