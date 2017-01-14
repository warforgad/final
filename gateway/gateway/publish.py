from . import mq

class Publish(mq.Publisher):
    EXCHANGE_NAME = 'events'

    @classmethod
    def init_publisher(cls, host):
        cls.publisher = mq.Publisher(cls.EXCHANGE_NAME, host)

    @classmethod
    def publish(cls, msg, routing_key=None):
        if hasattr(cls, 'publisher'):
            cls.publisher.publish(msg, routing_key=routing_key)
