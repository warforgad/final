import random
from . import plugin, plugins
from .publish import Publish
from .clientinfo import ClientInfo
from shortuuid import uuid

clients = {}

class NonExistingClientError(Exception):
    pass

def process_client(client_info):
    for matcher in plugin.matchers:
        command = matcher(client_info)
        if command != None:
            yield plugin.commands[command](client_info)

def generate_id(data):
    return uuid(data.name)

def generate_connected_event(client_info):
    return 'Client {} connected!'.format(client_info.name)

def send_nocontent(client_id):
    del clients[client_id]
    return {'id' : client_id, 'command': {'command': 'sleep', 'args': {'duration': random.randint(1,15)}}}

def send_command(client_id, client_info, command):
    client_info.command = command['command']
    return {'id' : client_id, 'command' : command}

def send_next_command(client_id, client_info):
    try:
        return send_command(client_id, client_info, next(client_info.context))
    except StopIteration:
        return send_nocontent(client_id)

def handle_submit(client_id, data):
    if not client_id in clients:
        raise NonExistingClientError()
    client_info = clients[client_id]
    command = plugin.reactors[client_info.command](client_info, data)
    if command != None:
        return send_command(client_id, client_info, plugin.commands[command](client_info))
    else:
        return send_next_command(client_id, client_info)

def handle_connection(client_info_dict):
    client_info = ClientInfo(client_info_dict)
    client_id = generate_id(client_info)
    clients[client_id] = client_info
    Publish.publish(generate_connected_event(client_info))
    client_info.context = process_client(client_info)        
    return send_next_command(client_id, client_info)
