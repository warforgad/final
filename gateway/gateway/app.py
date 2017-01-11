from flask import Flask, json, request
from . import server
my_app = Flask(__name__)

@my_app.route('/connect', methods=['POST'])
def client_connected():
    client_info = json.loads(request.data)
    return json.dumps(server.handle_connection(client_info))
    
@my_app.route('/bar')
def get_bar():
    return bar()
