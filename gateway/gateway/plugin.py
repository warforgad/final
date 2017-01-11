matchers = []
commands = {}
reactors = {}

class DuplicateNameError(Exception):
    pass

class matcher:
    
    def __init__(self, f):
        self.f = f
        matchers.append(self)

    def __call__(self, *args, **kwargs):
        return self.f(*args, **kwargs)

class command:

    def __init__(self, name):
        self.name = name

    def __call__(self, f):
        def decorated(*args, **kwargs):
            return f(*args, **kwargs)
        if self.name in commands:
            raise DuplicateNameError('There is already a command named {}!'.format(self.name))
        commands[self.name] = decorated
        return decorated

class reactor:

    def __init__(self, name):
        self.name = name

    def __call__(self, f):
        def decorated(*args, **kwargs):
            return f(*args, **kwargs)
        if self.name in reactors:
            raise DuplicateNameError('There is already a reactor named {}!'.format(self.name))
        reactors[self.name] = decorated
        return decorated
