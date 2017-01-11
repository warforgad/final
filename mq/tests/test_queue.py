import pika, pytest

MESSAGE = 'hello'

def test_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='test')
    channel.basic_publish(exchange='', routing_key='test', body=MESSAGE)
    
    for method_frame, properties, body in channel.consume('test'):
        assert body.decode() == MESSAGE
        channel.basic_ack(method_frame.delivery_tag)
        break
