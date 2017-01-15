import datetime, django, json, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saver.settings")
django.setup()
from subscriber import models, mq

MQ_HOST = 'mq'

def handle_connection_event(channel, method, properties, body):
    event = json.loads(body.decode())
    print(event)
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
    

def handle_command_event(channel, method, properties, body):
    event = json.loads(body.decode())
    connections_by_uuid = models.Connection.objects.filter(client_uuid=event['id'])
    if not connections_by_uuid.exists():
        # TODO non existing client
        pass
    models.Command(
        client=connections_by_uuid[0].client,
        command=event['command'],
        sent_time=datetime.datetime.fromtimestamp(event['timestamp']) 
    ).save()


def handle_result_event(channel, method, properties, body):
    event = json.loads(body.decode())
    connections_by_uuid = models.Connection.objects.filter(client_uuid=event['id'])
    if not connections_by_uuid.exists():
        # TODO non existing client
        pass
    models.Result(
        client=connections_by_uuid[0].client,
        command=event['command'],
        result=event['result'],
        received_time=datetime.datetime.fromtimestamp(event['timestamp']) 
    ).save()
    
def main():
    subsciber = mq.Subscriber(MQ_HOST)
    subsciber.register_callback(handle_connection_event, 'events', routing_key='connect', durable=True)
    subsciber.register_callback(handle_command_event, 'events', routing_key='command', durable=True)
    subsciber.register_callback(handle_result_event, 'events', routing_key='result', durable=True)
    subsciber.start_consuming()
    

if __name__ == '__main__':
    main()
