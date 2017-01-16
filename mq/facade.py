import json, pika

defaults = {
    'exclusive': False,
    'durable': False,
    'no_ack': False,
    'routing_key': '#',
    'callback_nack_requeue': True
}

class Callback:
    
    def __init__(self, callback):
        self.callback = callback

    def __call__(self, channel, method, properties, body):
        self.channel = channel
        self.method = method
        self.properties = properties
        self.body = body
        self.callback(self)

    def ack(self):
        self.channel.basic_ack(self.method.delivery_tag)

    def nack(self, requeue=None):
        if requeue is None:
            requeue = defaults['callback_nack_requeue']
        self.channel.basic_nack(self.method.delivery_tag)

    def get_json_event(self):
        return json.loads(self.body.decode())
        

def uses_connection(decorated):
    '''Decorator for member functions of objects with a 'connect' member function.
    It'll attempt to reconnect and block until a connected'''
    def safe(self, *args, **kwargs):
        while True:
            try:
                return decorated(self, *args, **kwargs) 
            except pika.exceptions.ConnectionClosed:
                self.connect()
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

class Publisher(QueueUser):

    def __init__(self, exchange, host):
        self.exchange = exchange
        super().__init__(host)

    def connect(self):
        '''Connects to the MQ and declares an exchange'''
        super().connect()
        self.channel.exchange_declare(exchange=self.exchange, type='topic')

    @uses_connection
    def publish(self, msg, routing_key=None):
        '''Publishes msg to the mq'''
        if routing_key is None:
            routing_key = ''
        return self.channel.basic_publish(exchange=self.exchange, routing_key=routing_key, body=msg) 

    def publish_json(self, msg_dict, routing_key=None):
        return self.publish(json.dumps(msg_dict), routing_key)

class Subscriber(QueueUser):
    def __init__(self, host):
        self.registered = []
        super().__init__(host)

    def connect(self):
        super().connect()
        for args in self.registered:
            self._setup(**args)

    def _setup(self, callback, exchange, routing_key=None, queue_name=None, no_ack=None, exclusive=None, durable=None):
        if no_ack is None:
            no_ack = defaults['no_ack']
        if exclusive is None:
            exclusive = defaults['exclusive']
        if durable is None:
            durable = defaults['durable']
        if routing_key is None:
            routing_key = defaults['routing_key']
        if queue_name is None:
            queue_name = self.channel.queue_declare().method.queue
        else:
            self.channel.queue_declare(queue=queue_name, exclusive=exclusive, durable=durable) 
        self.channel.exchange_declare(exchange=exchange, type='topic')
        self.channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=routing_key)
        if callback is not None:
            self.channel.basic_consume(callback, queue=queue_name, no_ack=no_ack)

    @uses_connection
    def register_callback(self, callback, exchange, routing_key=None, queue_name=None, no_ack=None, exclusive=None, durable=None):
        #TODO registering multiple callbacks for the same queue with different routing keys.
        callback_wrapper = Callback(callback)
        self._setup(callback_wrapper, exchange, routing_key, queue_name, no_ack, exclusive, durable)
        self.registered.append(
            {
                'callback': callback_wrapper,
                'exchange': exchange,
                'routing_key': routing_key,
                'no_ack': no_ack,
                'queue_name': queue_name,
                'exclusive': exclusive,
                'durable': durable
            }
        )

    @uses_connection
    def register_queue(self, exchange, routing_key=None, queue_name=None, no_ack=None, exclusive=None, durable=None):
        self._setup(None, exchange, routing_key, queue_name, no_ack, exclusive, durable)
        self.registered.append(
            {
                'callback': None,
                'exchange': exchange,
                'routing_key': routing_key,
                'no_ack': no_ack,
                'queue_name': queue_name,
                'exclusive': exclusive,
                'durable': durable
            }
        )

    @uses_connection
    def start_consuming(self):
        return self.channel.start_consuming()

    @uses_connection
    def basic_get(self, queue_name, no_ack):
        return self.channel.basic_get(queue=queue_name, no_ack=no_ack)
