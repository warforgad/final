import json, mq, pytest, requests
from gateway import server

def test_publish():
    subscriber = mq.Subscriber('localhost')
    subscriber.register_callback(None, 'events', queue_name='test', no_ack=True, routing_key='connect')

    client1 = {'name':'test', 'version':'123'}
    info1 = server.ClientInfo(client1)
    requests.post('http://localhost:8000/connect', json=client1)
    method_frame, properties, body = subscriber.basic_get('test', no_ack=True)
    assert not body is None and body.decode() == server.generate_connected_event(info1)

    client2 = {'name':'another test', 'version':'0'}
    info2 = server.ClientInfo(client2)
    requests.post('http://localhost:8000/connect', json=client2)
    method_frame, properties, body = subscriber.basic_get('test', no_ack=True)
    assert not body is None and body.decode() == server.generate_connected_event(info2)
