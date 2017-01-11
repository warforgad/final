from .plugin import matcher, command, reactor

@matcher
def test_matcher(client_info):
    if 'mark' in client_info.name:
        return 'test'
    return None

@matcher
def test_matcher2(client_info):
    return 'foo'

@command('test')
def test_command(client_info):
    return 'test'

@reactor('test')
def test_reactor(client_info, data):
    return 'foo'

@command('foo')
def test_command2(client_info):
    return 'foo'

@reactor('foo')
def test_reactor2(client_info, data):
    return None
