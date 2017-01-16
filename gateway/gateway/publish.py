import time
from . import mq
from .clientinfo import ClientInfo

EXCHANGE_NAME = 'events'
MQ_HOST = 'mq'

publisher = mq.Publisher(EXCHANGE_NAME, MQ_HOST)

def publish_connected_event(client_info):
    msg = {
        'name': client_info.name,
        'version': client_info.version,
        'id': client_info.id,
        'timestamp': time.time()
    }
    publisher.publish_json(msg, routing_key='connect')
   
def publish_command(client_info):
    msg = {
        'id': client_info.id,
        'command': client_info.command,
        'transaction': client_info.transaction,
        'timestamp': time.time()
    }
    publisher.publish_json(msg, routing_key='command')

def publish_result(client_info, result):
    msg = {
        'transaction': client_info.transaction,
        'result': result,
        'timestamp': time.time()
    }
    publisher.publish_json(msg, routing_key='result')
