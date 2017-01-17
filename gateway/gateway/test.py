import sockettransfer, redisdict
import redis
import sys
import json
if len(sys.argv) != 2:
    print('USAGE: {} <port>'.format(sys.argv[0]))
    exit(1)

class A:
    
    def __init__(self,a,b,c):
        self.a=a
        self.b=b
        self.c=c

def encode_data(d):
    return json.dumps(d.__dict__).encode()

def decode_data(d):
    des = json.loads(d.decode())
    tmp = A(**des)
    return tmp

port = int(sys.argv[1])
t = sockettransfer.SocketTransferer(port)
d = redisdict.RedisDict(t, encode_data, decode_data)
a = A(1,[2],{3:3})
r = redis.StrictRedis(host='localhost', port=6379)

#def main(port):
#    t = transfer.SocketTransferer(port)
#    r = redisdict.RedisDict(t)
#
#if __name__ == '__main__':
#    import sys
#    if len(sys.argv) != 2:
#        print('USAGE: {} <port>'.format(sys.argv[0]))
#        exit(1)
#    main(port=int(sys.argv[1]))
