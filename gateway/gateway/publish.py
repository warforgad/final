import json, time
from . import mq
from .clientinfo import ClientInfo

EXCHANGE_NAME = 'events'
MQ_HOST = 'mq'

publisher = mq.Publisher(EXCHANGE_NAME, MQ_HOST)

def publish_connected_event(client_id, client_info):
    msg = json.dumps({
        'name': client_info.name,
        'version': client_info.version,
        'id': client_id,
        'timestamp': time.time()
    })
    publisher.publish(msg, routing_key='{}.connect'.format(EXCHANGE_NAME))
   
def publish_command(client_id, command):
    msg = json.dumps({
        'id': client_id,
        'command': command,
        'timestamp': time.time()
    })
    publisher.publish(msg, routing_key='{}.command'.format(EXCHANGE_NAME))

def publish_result(client_id, command, result):
    msg = json.dumps({
        'id': client_id,
        'command': command,
        'result': result,
        'timestamp': time.time()
    })
    publisher.publish(msg, routing_key='{}.result'.format(EXCHANGE_NAME))
