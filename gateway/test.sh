#!/bin/bash

SETUP=$1
TEARDOWN=$2

$SETUP
docker exec gateway_container pytest /tests --cov=/gateway
docker exec gateway_container coveralls
$TEARDOWN    
