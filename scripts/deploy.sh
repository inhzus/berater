#!/usr/bin/env bash
source env/bin/activate
scp berater/secret.py suun@weixinbak.njunova.com:~/
ssh suun@weixinbak.njunova.com "
cd ~/berater;
source env/bin/activate;
git fetch;
git reset origin/master --hard;
git clean -df;
mv ~/secret.py berater/secret.py;
pip3 install -r requirements.txt;
"
