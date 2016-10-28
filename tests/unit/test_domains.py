import datetime
from messaging.domains import Message


class TestMessage(object):
    def test_body_exceeds_max_chars(self):
        msg = Message(sender='21981527318', receiver='21980072800', body='a' * 161)
        assert msg.is_large() is True

    def test_body_does_not_exceed_max_chars(self):
        msg = Message(sender='21981527318', receiver='21980072800', body='Hello!')
        assert msg.is_large() is False

    def test_message_is_expired(self):
        msg = Message(sender='21981527318', receiver='21980072800', body='Hello!',
                expiration_date=yesterday())
        assert msg.is_expired() is True

    def test_message_is_not_expired(self):
        msg = Message(sender='21981527318', receiver='21980072800', body='Hello!',
                expiration_date=tomorrow())
        assert msg.is_expired() is False


def yesterday():
    return datetime.datetime.now() - datetime.timedelta(days=1)


def tomorrow():
    return datetime.datetime.now() + datetime.timedelta(days=1)
