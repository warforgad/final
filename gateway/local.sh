#!/bin/bash

MQ_CONTAINER='mq_container'
GATEWAY_CONTAINER='gateway_container'
SCRIPT_DIR=`dirname $0`

if [[ $* == *--debug* ]]; then
    DETACHED=''
else
    DETACHED='-d'
fi

echo "Killing old mq container..."
docker ps -aq -f name=$MQ_CONTAINER | xargs docker rm -f
echo "Running mq container... "
docker run -d --name=$MQ_CONTAINER -p 5672:5672 rabbitmq
echo "Killing old container..."
docker ps -aq -f name=$GATEWAY_CONTAINER | xargs docker rm -f
echo "Building image..."
docker build -t final_gateway $SCRIPT_DIR
echo "Running... "
MQ_IP=`docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $MQ_CONTAINER`
docker run $DETACHED -ti -p 8000:80 --name $GATEWAY_CONTAINER --add-host="mq:$MQ_IP" final_gateway
docker ps -a
