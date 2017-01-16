import mq, time
from shortuuid import uuid

publisher = mq.Publisher('events', 'localhost')

try:
    while True:
        ID = uuid()
        event = {'name': 'test', 'version': 'test', 'id': ID, 'timestamp': time.time()}
        publisher.publish_json(event, routing_key='connect')

        transaction_id = uuid()
        event = {'id': ID, 'command': 'foo', 'transaction': transaction_id, 'timestamp': time.time()}
        publisher.publish_json(event, routing_key='command')
        event = {'transaction': transaction_id, 'result': 'foo', 'timestamp': time.time()}
        publisher.publish_json(event, routing_key='result')

        transaction_id = uuid()
        event = {'id': ID, 'command': 'bar', 'transaction': transaction_id, 'timestamp': time.time()}
        publisher.publish_json(event, routing_key='command')
        event = {'transaction': transaction_id, 'result': 'bar', 'timestamp': time.time()}
        publisher.publish_json(event, routing_key='result')

        transaction_id = uuid()
        event = {'id': ID, 'command': 'sleep', 'transaction': transaction_id, 'timestamp': time.time()}
        publisher.publish_json(event, routing_key='command')
        time.sleep(5)
except KeyboardInterrupt:
    pass
