from . import plugin
from .publish import Publish
from .clientinfo import ClientInfo
from shortuuid import uuid

clients = {}

def import_plugins():
    from . import test_plugin

def process_client(client_info):
    for matcher in plugin.matchers:
        command = matcher(client_info)
        if command != None:
            yield plugin.commands[command](client_info)

def generate_id(data):
    return uuid(data.name)

def generate_connected_event(client_info):
    return 'Client {} connected!'.format(client_info.name)

def handle_connection(client_info_dict):
    client_info = ClientInfo(client_info_dict)
    client_id = generate_id(client_info)
    clients[client_id] = client_info
    Publish.publish(generate_connected_event(client_info))
    client_info.context = process_client(client_info)        
    try:
        command = next(client_info.context)
        return {'id' : client_id, 'command' : command}
    except StopIteration:
        #TODO send sleep
        return {'id': client_id, 'command': 'sleep'}
