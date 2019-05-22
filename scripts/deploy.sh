#!/usr/bin/env bash
source env/bin/activate
scp .env suun@weixinbak.njunova.com:~/
ssh suun@weixinbak.njunova.com "
cd ~/berater;
git fetch;
git reset origin/master --hard;
git clean -df;
mv ~/.env ./;
"
