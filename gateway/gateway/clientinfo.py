import random
from shortuuid import uuid
from . import plugin, plugins

clients = {}

class ClientInfo:
    
    def __init__(self, info_dict, client_id):
        self.name = info_dict['name']
        self.version = info_dict['version']
        self.id = client_id
        self.command = None
        self.transaction = None
        self.context = self.generate_context()

    @staticmethod
    def from_id(client_id):
        return clients.get(client_id)

    @classmethod
    def new_client(cls, info_dict):
        client_id = uuid()
        client = cls(info_dict, client_id)
        clients[client_id] = client
        return client

    def generate_context(self):
        for matcher in plugin.matchers:
            command = matcher(self)
            if command is not None:
                yield plugin.commands[command](self)

    def create_command(self, command):
        if command is None:
            return {'id': self.id, 'command': self.create_nocontent()}
        self.command = command['command']
        self.transaction = uuid()
        return {'id' : self.id, 'command' : command}

    def create_nocontent(self):
        del clients[self.id]
        return {'command': 'sleep', 'args': {'duration': random.randint(1,15)}}

    def create_next_command(self):
        return self.create_command(next(self.context, None))

    def process_result(self, result):
        command = plugin.reactors[self.command](self, result)
        if command != None:
            return self.create_command(plugin.commands[command](self))
        else:
            return self.create_next_command()
            
