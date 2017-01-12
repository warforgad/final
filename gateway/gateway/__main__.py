from . import server
from .publish import Publish
from .app import my_app

MQ_HOST = 'mq'

if __name__ == '__main__':
    Publish.init_publisher(MQ_HOST) 
    server.import_plugins()
    my_app.run(host='0.0.0.0', port=80)