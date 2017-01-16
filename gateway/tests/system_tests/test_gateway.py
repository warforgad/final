import json, mq, pytest, requests

def test_publish():
    subscriber = mq.Subscriber('localhost')
    subscriber.register_queue('events', queue_name='test', no_ack=True, routing_key='connect')

    client1 = {'name':'test', 'version':'123'}
    requests.post('http://localhost:8000/connect', json=client1)
    body = subscriber.basic_get('test', no_ack=True)[2]
    assert not body is None 
    event = json.loads(body.decode())
    assert event['name'] == client1['name'] and event['version'] == client1['version']

    client2 = {'name':'another test', 'version':'0'}
    requests.post('http://localhost:8000/connect', json=client2)
    body = subscriber.basic_get('test', no_ack=True)[2]
    assert not body is None 
    event = json.loads(body.decode())
    assert event['name'] == client2['name'] and event['version'] == client2['version']
