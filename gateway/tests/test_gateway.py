import json, mq, pytest, requests
from gateway import server

def test_publish():
    print('subscriber...')
    subscriber = mq.Subscriber('events', 'mq')
    client1 = {'name':'test', 'version':'123'}
    info1 = server.ClientInfo(client1)
    print('connect...')
    requests.post('http://localhost:80/connect', json=client1)
    print('consuming...')
    method_frame, properties, body = next(subscriber.consume())
    assert body.decode() == server.generate_connected_event(info1)
    print('consumed')

    client2 = {'name':'another test', 'version':'0'}
    info2 = server.ClientInfo(client2)
    requests.post('http://localhost:80/connect', json=client2)
    method_frame, properties, body = next(subscriber.consume())
    assert body.decode() == server.generate_connected_event(info2)


def test_reactor():
    #connect
    client = {'name':'mark', 'version':'1.0'}
    r = requests.post('http://localhost:80/connect', json=client)
    assert r.status_code == 200 
    r_data = json.loads(r.text)
    info = server.ClientInfo(client)
    assert r_data['id'] == server.generate_id(info) and r_data['command'] == 'test'

    #non connected client
    fake_submit = {'id' : 'lelelelelelelel', 'data' : 'lololololol' }
    r = requests.post('http://localhost:80/submit', json=fake_submit)
    assert r.status_code == 204 

    #submit result and follow reactor chain
    submitted = {'id' : r_data['id'], 'data':'hello'}
    r = requests.post('http://localhost:80/submit', json=submitted)
    assert r.status_code == 200 
    r_data = json.loads(r.text)
    assert r_data['id'] == server.generate_id(info) and r_data['command'] == 'foo'

    r = requests.post('http://localhost:80/submit', json=submitted)
    assert r.status_code == 200 
    r_data = json.loads(r.text)
    assert r_data['id'] == server.generate_id(info) and r_data['command'] == 'foo'

    r = requests.post('http://localhost:80/submit', json=submitted)
    assert r.status_code == 200 
    r_data = json.loads(r.text)
    assert r_data['command'] == 'sleep'

    #test end of chain
    r = requests.post('http://localhost:80/submit', json=submitted)
    assert r.status_code == 204 

