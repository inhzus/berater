FROM python:3.6

WORKDIR /berater

ADD ./requirements.txt /berater

RUN pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

COPY ./berater /berater

COPY ./conf/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

ENV FLASK_APP=/berater/app.py
ENV FLASK_ENV=development

RUN apt update
RUN apt install -y supervisor

