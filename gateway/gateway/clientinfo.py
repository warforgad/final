class ClientInfo:
    
    def __init__(self, info_dict):
        self.name = info_dict['name']
        self.version = info_dict['version']
        self.context = None
