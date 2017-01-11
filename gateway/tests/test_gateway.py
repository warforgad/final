import mq, pytest, requests
from gateway import server

def test_connect():
    subscriber = mq.Subscriber('events', 'localhost')
    client1 = {'name':'test'}
    requests.post('http://localhost:8000/connect', json=client1)
    method_frame, properties, body = next(subscriber.consume())
    assert body.decode() == server.generate_connected_event(client1)

    client2 = {'name':'another test'}
    requests.post('http://localhost:8000/connect', json=client2)
    method_frame, properties, body = next(subscriber.consume())
    assert body.decode() == server.generate_connected_event(client2)
