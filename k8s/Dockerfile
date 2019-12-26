FROM python:3.6

LABEL maintainer="sqe_cvs@nio.com"

# Add custom china source
ADD ./k8s/sources.list /etc/apt/

# copy source code
COPY . /opt/performance_test

# install package
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y net-tools
RUN pip3 install paho-mqtt gevent hbmqtt

CMD /bin/bash
