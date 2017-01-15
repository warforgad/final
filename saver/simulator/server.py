import mq, time

publisher = mq.Publisher('events', 'localhost')

try:
    while True:
        ID = 22*'a'
        event = {'name': 'test', 'version': 'test', 'id': ID, 'timestamp': time.time()}
        publisher.publish_json(event, routing_key='connect')
        event = {'id': ID, 'command': 'foo', 'timestamp': time.time()}
        publisher.publish_json(event, routing_key='command')
        event = {'id': ID, 'command': 'foo', 'result': 'foo', 'timestamp': time.time()}
        publisher.publish_json(event, routing_key='result')
        event = {'id': ID, 'command': 'bar', 'timestamp': time.time()}
        publisher.publish_json(event, routing_key='command')
        event = {'id': ID, 'command': 'bar', 'result': 'bar', 'timestamp': time.time()}
        publisher.publish_json(event, routing_key='result')
        event = {'id': ID, 'command': 'sleep', 'timestamp': time.time()}
        publisher.publish_json(event, routing_key='command')
        time.sleep(5)
except KeyboardInterrupt:
    pass
