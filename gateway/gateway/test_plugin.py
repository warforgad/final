from .plugin import matcher, command

@matcher
def test_matcher(client_info):
    if 'mark' in client_info.name:
        return 'test'
    return None

@command('test')
def test_command(client_info):
    return 'test'
