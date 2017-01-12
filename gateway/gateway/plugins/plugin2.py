from . import plugin

@plugin.matcher
def matcher(client_info):
    if len(client_info.name) == 6:
        return 'calc'

@plugin.command('calc')
def command(client_info):
    return 'calc'

@plugin.reactor('calc')
def reactor(client_info, data):
    return None
