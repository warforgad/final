from .publish import Publish
from flask import json
from shortuuid import uuid
clients = {}

def generate_id(data):
    return uuid(data['name'])

def generate_connected_event(client_info):
    return 'Client {} connected!'.format(client_info['name'])

def handle_connection(client_info):
    client_id = generate_id(client_info)
    clients[client_id] = client_info
    Publish.publish(generate_connected_event(client_info))
    return {'id' : client_id}
