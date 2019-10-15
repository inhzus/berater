FROM python:3.6

WORKDIR /berater

ADD ./requirements.txt /berater
#RUN pip install pip -U  -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U
#RUN pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY ./berater /berater
COPY ./data /data

COPY ./conf/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

ENV FLASK_APP=/berater/app.py
ENV FLASK_ENV=production

