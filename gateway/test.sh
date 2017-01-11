#!/bin/bash

SETUP=$1
TESTS=$2
CODE=$3
TEARDOWN=$4

$SETUP
pytest $TESTS --cov=$CODE
$TEARDOWN    
