#!/bin/bash

# exit on error
set -e

# the script's dir
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# setup
#$DIR/local.sh
docker-compose up -d --build
# run unit tests
#docker exec gateway_container pytest /tests --cov=/gateway
docker-compose exec gateway1 pytest /tests --cov=/gateway
#docker exec gateway_container coveralls
# run system tests
pytest $DIR/tests/system_tests
# teardown
#$DIR/teardown.sh
docker-compose down
