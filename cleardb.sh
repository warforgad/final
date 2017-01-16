#!/bin/bash

 
psql -h localhost -U postgres -d postgres -c 'DELETE FROM subscriber_result;'
psql -h localhost -U postgres -d postgres -c 'DELETE FROM subscriber_command;'
psql -h localhost -U postgres -d postgres -c 'DELETE FROM subscriber_connection;'
psql -h localhost -U postgres -d postgres -c 'DELETE FROM subscriber_client;'
