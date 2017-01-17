import json, random
from shortuuid import uuid
from . import plugin, plugins, redisdict, sockettransfer

def encode_data(client_info):
    return json.dumps(client_info.__dict__).encode()
    
def decode_data(json_info):
    tmp = ClientInfo({'name':'', 'version':''}, '')
    tmp.__dict__.update(**json.loads(json_info.decode()))
    return tmp

TRANSFER_PORT = 9000
clients = redisdict.RedisDict(sockettransfer.SocketTransferer(TRANSFER_PORT), encode_data, decode_data)

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
        return clients[client_id]

    @classmethod
    def new_client(cls, info_dict):
        client_id = uuid()
        client = cls(info_dict, client_id)
        clients[client_id] = client
        return client

    def generate_context(self):
        return list(plugin.matchers.keys())

    def create_command(self, command):
        if command is None:
            return {'id': self.id, 'command': self.create_nocontent()}
        self.command = command['command']
        self.transaction = uuid()
        return {'id' : self.id, 'command' : command}

    def create_nocontent(self):
        del clients[self.id]
        self.command = 'sleep'
        self.transaction = uuid()
        return {'command': 'sleep', 'args': {'duration': random.randint(1,15)}}

    def create_next_command(self):
        while True:
            if len(self.context) == 0:
                return None
            next_matcher = self.context.pop()
            next_command = plugin.matchers[next_matcher](self)
            if next_command is not None:
                return self.create_command(plugin.commands[next_command](self))

    def process_result(self, result):
        command = plugin.reactors[self.command](self, result)
        if command != None:
            return self.create_command(plugin.commands[command](self))
        else:
            return self.create_next_command()

            
