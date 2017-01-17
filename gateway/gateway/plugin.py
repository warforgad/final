matchers = {}
commands = {}
reactors = {}

def matcher(name):
    def matcher_decorator(decorated):
        if name in matchers:
            raise ValueError('There is already a matcher named {}!'.format(name))
        matchers[name] = decorated
        return decorated
    return matcher_decorator

def command(name):
    def command_decorator(decorated):
        if name in commands:
            raise ValueError('There is already a command named {}!'.format(name))
        commands[name] = decorated
        return decorated
    return command_decorator

def reactor(name):
    def reactor_decorator(decorated):
        if name in reactors:
            raise ValueError('There is already a reactor named {}!'.format(name))
        reactors[name] = decorated
        return decorated
    return reactor_decorator
