from . import plugin 

@plugin.matcher
def test_matcher(client_info):
    if 'mark' in client_info.name:
        return 'test'
    return None

@plugin.matcher
def test_matcher2(client_info):
    return 'foo'

@plugin.command('test')
def test_command(client_info):
    return 'test'

@plugin.reactor('test')
def test_reactor(client_info, data):
    return 'foo'

@plugin.command('foo')
def test_command2(client_info):
    return 'foo'

@plugin.reactor('foo')
def test_reactor2(client_info, data):
    return None
