import datetime, django, json, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saver.settings")
django.setup()
from subscriber import models, mq

MQ_HOST = 'mq'

def callback(channel, method, properties, body):
    event = json.loads(body.decode())
    # Get or create the client
    client, created = models.Client.objects.get_or_create(
        client_name=event['name'],
        client_version=event['version'],
        defaults={'created_time': datetime.datetime.fromtimestamp(event['timestamp'])}
    )
        
    # Add connection
    models.Connection(
        client=client,
        client_uuid=event['id'],
        connection_time=datetime.datetime.fromtimestamp(event['timestamp'])
    ).save()
    
    
def main():
    subsciber = mq.Subscriber(MQ_HOST)
    subsciber.register_callback(callback, 'events', queue_name='saver', routing_key='connect', durable=True)
    subsciber.start_consuming()
    

if __name__ == '__main__':
    main()
