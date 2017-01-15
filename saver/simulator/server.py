import json, mq, time

publisher = mq.Publisher('events', 'localhost')

try:
    while True:
       event = {'name': 'test', 'version': 'test', 'id': 22*'a', 'timestamp': time.time()}
       publisher.publish(json.dumps(event), routing_key='connect')
       time.sleep(5)
except KeyboardInterrupt:
    pass
