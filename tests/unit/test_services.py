import datetime
import pytest
from unittest import mock

from messaging.services import MessageTooLargeError, ExpiredMessageError, SendMessageService


def test_can_send():
    ms = SendMessageService(mock.Mock(), mock.Mock())
    ms.send(id=100, sender='21981527318', receiver='21981211250', body='Hello!')


def test_cannot_send_messages_larger_than_160_chars():
    with pytest.raises(MessageTooLargeError) as e:
        ms = SendMessageService(mock.Mock(), mock.Mock())
        ms.send(id=100, sender='21981527318', receiver='21981211250', body='x'*161)


def test_cannot_send_expired_messages():
    with pytest.raises(ExpiredMessageError) as e:
        ms = SendMessageService(mock.Mock(), mock.Mock())
        ms.send(id=100, sender='21981527318', receiver='21981211250', body='Hello!', expiration_date=old_date())


def test_should_create_message():
    r = mock.Mock()

    ms = SendMessageService(r, mock.Mock())
    ms.send(id=100, sender='21981527318', receiver='21981211250', body='Hello!')

    r.create.assert_called_with('21981527318', '21981211250', 'Hello!', None)


def test_should_send_message_to_the_operator_api():
    m = mock.Mock()

    ms = SendMessageService(mock.Mock(), m)
    ms.send(id=100, sender='21981527318', receiver='21981211250', body='Hello!')

    m.send.assert_called_with(100, '21981527318', '21981211250', 'Hello!')


# def test_should_mark_message_as_delivered():
#     r = mock.Mock()
#     message = r.create.return_value = mock.Mock()
#
#     ms = SendMessageService(r, mock.Mock())
#     ms.send(id=100, sender='21981527318', receiver='21981211250', body='Hello!')
#
#     r.mark_as_delivered.assert_called_with(message)


def test_should_update_status():
    r = mock.Mock()
    message = r.create.return_value = mock.Mock()

    m = mock.Mock()

    ms = SendMessageService(r, m)
    ms.send(id=100, sender='21981527318', receiver='21981211250', body='Hello!')

    r.update_status.assert_called_with(message.id, m.send.return_value.status_code)


# Helpers
# -------------------------------------------------------------------------------------------------

def old_date():
    return datetime.datetime.now() - datetime.timedelta(days=1)
