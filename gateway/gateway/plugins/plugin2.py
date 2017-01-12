from . import plugin

@plugin.matcher
def matcher(client_info):
    if len(client_info.name) == 6:
        return 'calc'

@plugin.command('calc')
def command(client_info):
    return {'command': 'calc', 'args': {'number': 5}}

@plugin.reactor('calc')
def reactor(client_info, data):
    return None
