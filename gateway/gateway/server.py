from . import publish
from . import clientinfo

class NonExistingClientError(Exception):
    pass

def handle_submit(client_id, data):
    client_info = clientinfo.ClientInfo.from_id(client_id)
    if client_info is None:
        raise NonExistingClientError()
    publish.publish_result(client_info, data)
    next_command = client_info.process_result(data)
    publish.publish_command(client_info)
    return next_command

def handle_connection(client_info_dict):
    client_info = clientinfo.ClientInfo.new_client(client_info_dict)
    publish.publish_connected_event(client_info)
    next_command = client_info.create_next_command()
    publish.publish_command(client_info)
    return next_command
