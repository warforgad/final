import datetime, django, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saver.settings")
django.setup()
from subscriber import models, mq

MQ_HOST = 'mq'

def handle_connection_event(event):
    try:
        event_data = event.get_json_event()
        # Get or create the client
        client, created = models.Client.objects.get_or_create(
            client_name=event_data['name'],
            client_version=event_data['version'],
            defaults={'created_time': datetime.datetime.fromtimestamp(event_data['timestamp'])}
        )
            
        # Add connection
        models.Connection(
            client=client,
            client_uuid=event_data['id'],
            connection_time=datetime.datetime.fromtimestamp(event_data['timestamp'])
        ).save()
        event.ack() 
    except Exception:
        event.nack()

def handle_command_event(event):
    event_data = event.get_json_event()
    try:
        connection = models.Connection.objects.get(client_uuid=event_data['id'])
        models.Command(
            connection=connection,
            command=event_data['command'],
            transaction_uuid=event_data['transaction'],
            sent_time=datetime.datetime.fromtimestamp(event_data['timestamp']) 
        ).save()
        event.ack()
    except models.Connection.DoesNotExist:
        #TODO
        event.ack()
    except Exception:
        event.nack()


def handle_result_event(event):
    event_data = event.get_json_event()
    try:
        command = models.Command.objects.get(transaction_uuid=event_data['transaction'])

        # The result could be empty
        if event_data['result'] is None:
            event_data['result'] = ''

        models.Result(
            command=command,
            result=event_data['result'],
            received_time=datetime.datetime.fromtimestamp(event_data['timestamp']) 
        ).save()
    except models.Command.DoesNotExist:
        #TODO
        event.ack()
    except Exception:
        event.nack()
    
def main():
    subsciber = mq.Subscriber(MQ_HOST)
    subsciber.register_callback(handle_connection_event, 'events', routing_key='connect', durable=True)
    subsciber.register_callback(handle_command_event, 'events', routing_key='command', durable=True)
    subsciber.register_callback(handle_result_event, 'events', routing_key='result', durable=True)
    subsciber.start_consuming()
    

if __name__ == '__main__':
    main()
