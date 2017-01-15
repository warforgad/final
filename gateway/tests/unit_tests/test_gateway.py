import json, mq, pytest, requests
from gateway import clientinfo, app

def test_connect():
    client = {'name':'mark', 'version':'1.0'}

    with app.my_app.test_client() as c:
        rv = c.post('/connect', data=json.dumps(client), content_type='application/json')
        assert rv.status_code == 200 and json.loads(rv.data.decode())['id'] == clientinfo.ClientInfo.generate_id(client)

def test_reactor_chain():
    client = {'name':'mark', 'version':'1.0'}

    with app.my_app.test_client() as c:
        #connect
        rv = c.post('/connect', data=json.dumps(client), content_type='application/json')
        assert rv.status_code == 200 
        r_data = json.loads(rv.data.decode())
        assert r_data['command']['command'] == 'test'

        #non connected client
        fake_submit = {'id' : 'lelelelelelelel', 'data' : 'lololololol' }
        rv = c.post('/submit', data=json.dumps(fake_submit), content_type='application/json')
        assert rv.status_code == 204 

        #submit result and follow reactor chain
        submitted = {'id' : r_data['id'], 'data':'hello'}
        rv = c.post('/submit', data=json.dumps(submitted), content_type='application/json')
        assert rv.status_code == 200 
        r_data = json.loads(rv.data.decode())
        assert r_data['command']['command'] == 'foo'

        rv = c.post('/submit', data=json.dumps(submitted), content_type='application/json')
        assert rv.status_code == 200 
        r_data = json.loads(rv.data.decode())
        assert r_data['command']['command'] == 'foo'

        rv = c.post('/submit', data=json.dumps(submitted), content_type='application/json')
        assert rv.status_code == 200 
        r_data = json.loads(rv.data.decode())
        assert r_data['command']['command'] == 'sleep'

        #test end of chain
        rv = c.post('/submit', data=json.dumps(submitted), content_type='application/json')
        assert rv.status_code == 204 

