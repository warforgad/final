FROM ubuntu
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y python3 python3-dev python3-pip libpq-dev
ADD requirements.txt /
RUN pip3 install -r requirements.txt
ADD mq mq
RUN export PYTHONPATH=$PYTHONPATH:/mq
