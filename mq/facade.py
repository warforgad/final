import pika

def uses_connection(decorated):
    '''Decorator for member functions of objects with 'is_connected' and 'connect' member function.
    It'll attempt to reconnect and block until a connected'''
    def safe(self, *args, **kwargs):
        while not self.is_connected():
            self.connect()
        return decorated(self, *args, **kwargs)
    return safe

class QueueUser():

    def __init__(self, host):
        '''Initializes a queue user and connects to the MQ'''
        self.host = host
        self.connect()

    def connect(self):
        '''Connects to the MQ'''
        while True:
            try:
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
                break
            except pika.exceptions.ConnectionClosed:
                pass
            # XXX 
            # There is a bug in pika where the connection state isn't properly cleaned after a failed connect.
            # This causes an IncompatibleProtocolError, so we must ignore it.
            except pika.exceptions.IncompatibleProtocolError:
                pass
        self.channel = self.connection.channel()

    def is_connected(self):
        '''Returns True iff the connection to the queue is still active'''
        return self.connection.is_open

class Publisher(QueueUser):

    def __init__(self, exchange, host):
        self.exchange = exchange
        super().__init__(host)

    def connect(self):
        '''Connects to the MQ and declares an exchange'''
        super().connect()
        self.channel.exchange_declare(exchange=self.exchange, type='fanout')

    @uses_connection
    def publish(self, msg):
        '''Publishes msg to the mq'''
        return self.channel.basic_publish(exchange=self.exchange, routing_key='', body=msg) 

class Subscriber(QueueUser):
    def __init__(self, exchange, host):
        self.exchange = exchange
        super().__init__(host)

    def connect(self):
        super().connect()
        self.channel.exchange_declare(exchange=self.exchange, type='fanout')
        self.queue_name = self.channel.queue_declare(exclusive=True).method.queue
        self.channel.queue_bind(exchange=self.exchange, queue=self.queue_name)

    @uses_connection
    def register_callback(self, callback):
        return self.channel.basic_consume(callback, queue=self.queue_name, no_ack=True)

    @uses_connection
    def start_consuming(self):
        return self.channel.start_consuming()

    @uses_connection
    def consume(self):
        return self.channel.consume(self.queue_name)
