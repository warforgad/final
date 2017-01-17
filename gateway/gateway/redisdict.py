import redis, threading

REDIS_HOST='redis'
REDIS_PORT=6379

class Empty():
   
    def encode(self):
        return b''

    def decode(self):
        return ''

class RedisDict():
    
    EMPTY = Empty()
   
    def __init__(self, transferer, encode_data, decode_data):
        self.data = {}
        self.mutex = threading.Lock()
        self.transferer = transferer
        self.encode_data = encode_data
        self.decode_data = decode_data
        self._redis = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
        self.listener = self.create_listener()

    def __getitem__(self, key):
        with self.mutex:
            self.take_ownership(key)
            val = self.data[key]
        if val == self.EMPTY:
            return None
        return val

    def __setitem__(self, key, value):
        with self.mutex:
            self.take_ownership(key)
            self.data[key] = value

    def __delitem__(self, key):
        with self.mutex:
            self.take_ownership(key)
            self._redis.delete(key)
            del self.data[key]

    def take_ownership(self, key):
        if key in self.data:
            return
        token = self._redis.getset(key, self.transferer.token)
        if token is None:
            self.data[key] = self.EMPTY
        else:
            #TODO handle Empty
            self.transferer.request(token.decode(), self.data, key, self.decode_data)

    def create_listener(self):
        t = threading.Thread(target=self.transferer.listen, args=(self.data, self.encode_data))
        t.start()
        return t
        
