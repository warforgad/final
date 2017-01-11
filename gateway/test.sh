#!/bin/bash

./local.sh
pytest ./tests --cov=./gateway
./teardown.sh
