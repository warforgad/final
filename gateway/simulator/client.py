import json, requests, time

HOST='localhost'
PORT='9000'
URL='http://{}:{}/'.format(HOST, PORT)

def foo():
    print('foo')
    return 'foo'

def test():
    print('test')

def calc(number):
    print('calc', number)
    return number

def sleep(duration):
    print('sleeping {} seconds...'.format(duration))
    time.sleep(duration)
    print('woke up!')

commands = {
    'foo'   : foo,
    'test'  : test,
    'calc'  : calc,
    'sleep' : sleep
}

class Client:
    
    def __init__(self, name, version):
        self.name = name
        self.version = version
        self.commands = commands
        self.connected = False

    def loop(self):
        while True:
            print('Connecting...')
            self.id, command = self.connect()
            print(command)
            print('Connected! Got id {}'.format(self.id))
            while True:
                print('Doing command {}'.format(command['command']))
                result = self.do_command(command)
                if not self.connected:
                    break
                print('Submitting result {}'.format(result))
                self.id, command = self.submit(result)
            print('Starting over')
            #DEBUG
            return
        
    def do_command(self, command):
        if command['command'] == 'sleep':
            print('changed')
            self.connected = False
        return self.commands[command['command']](**command['args'])

    def connect(self):
        r = requests.post(URL + 'connect', json={'name':self.name, 'version':self.version})
        if r.status_code != 200:
            raise Exception('Got status code {} for connect'.format(r.status_code))
        self.connected = True
        response = json.loads(r.text)
        return response['id'], response['command'] 
    
    def submit(self, result):
        r = requests.post(URL + 'submit', json={'id':self.id, 'data':result})
        if r.status_code != 200:
            raise Exception('Got status code {} for submit'.format(r.status_code))
        response = json.loads(r.text)
        return response['id'], response['command']

def main(name, version):
    client = Client(name, version)
    client.loop()

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print('USAGE: {} <name> <version>'.format(sys.argv[0]))
        exit(1)
    main(name=sys.argv[1], version=sys.argv[2])
        
