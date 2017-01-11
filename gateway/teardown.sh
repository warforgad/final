#!/bin/bash

MQ_CONTAINER='mq_container'
GATEWAY_CONTAINER='gateway_container'

echo "Killing old mq container..."
docker ps -aq -f name=$MQ_CONTAINER | xargs docker rm -f
echo "Killing old container..."
docker ps -aq -f name=$GATEWAY_CONTAINER | xargs docker rm -f
