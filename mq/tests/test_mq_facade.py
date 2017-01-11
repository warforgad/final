import mq_facade

MESSAGE = 'test message'

def test_facade():
    publisher = mq_facade.Publisher('test')
    subscriber = mq_facade.Subscriber('test')
    publisher.publish(MESSAGE)
    method_frame, properties, body = subscriber.consume().next()
    assert body.decode() == MESSAGE
