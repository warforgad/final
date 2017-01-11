import mq_facade

MESSAGE = 'test message'

def test_facade():
    publisher = mq_facade.Publisher('test')
    subscriber = mq_facade.Subscriber('test')
    publisher.publish(MESSAGE)
    for method_frame, properties, body in subscriber.consume():
        assert body.decode() == MESSAGE
        break
