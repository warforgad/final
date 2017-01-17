import json, socket, struct
from cached_property import cached_property

PORT = 9999
SIZE_PACK = 'I'

class SocketTransferer:
    
    def __init__(self, port):
        self.port = port

    @cached_property
    def token(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Fake random address.
            s.connect(('10.255.255.255', 0))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return '{}:{}'.format(IP, self.port)

    def request(self, token, local_dict, key, decode_data):
        s = socket.socket()
        host, port = token.split(':')
        s.connect((host, int(port)))
        send_with_header(s, key.encode())
        local_dict[key] = decode_data(recv_with_header(s))
        s.close()

    def listen(self, local_dict, encode_data):
        listener = socket.socket()
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(('0.0.0.0', self.port))
        listener.listen(10)
        while True:
            conn, addr = listener.accept()
            key = recv_with_header(conn).decode()
            send_with_header(conn, encode_data(local_dict[key]))
            del local_dict[key]
            conn.close()

def send_with_header(sock, data):
    sock.send(struct.pack(SIZE_PACK, len(data)))
    sock.send(data)

def recv_with_header(sock):
    data_size = struct.unpack(SIZE_PACK, sock.recv(struct.calcsize(SIZE_PACK)))[0]
    data = b''
    while len(data) < data_size:
        data = data + sock.recv(data_size - len(data))
    return data
