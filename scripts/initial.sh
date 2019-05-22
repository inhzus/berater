#!/usr/bin/env bash
scp .env suun@weixinbak.njunova.com:~/
ssh suun@weixinbak.njunova.com "
rm -rf berater;
git clone https://github.com/inhzus/berater;
cd berater;
mv ~/.env ./;
"
