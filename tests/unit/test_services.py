import datetime
import pytest

try:
    from unittest import mock
except ImportError:
    import mock

from messaging.services import MessageTooLargeError, ExpiredMessageError, SendMessageService


def test_should_raise_exception_when_body_is_larger_than_160_chars():
    with pytest.raises(MessageTooLargeError):
        ms = SendMessageService()
        ms.send(sender='21981527318', receiver='21981211250', body='x' * 161)


def test_should_raise_exception_when_expiration_date_is_an_old_date():
    with pytest.raises(ExpiredMessageError):
        ms = SendMessageService()
        ms.send(sender='21981527318', receiver='21981211250', body='Hello!', expiration_date=old_date())


def test_can_send(mocker):
    operator_api = mocker.patch('messaging.services.OperatorAPI')
    operator_api.return_value.send_sms.return_value = mock.Mock(status_code=201)
    repo = mocker.patch('messaging.services.MessageRepository')
    repo.return_value.create.return_value = mock.Mock()

    ms = SendMessageService()
    ms.send(sender='21981527318', receiver='21980072800', body='Hello!')

    repo.return_value.create.assert_called_with('21981527318', '21980072800', 'Hello!', None)


def test_should_persist_message(mocker):
    operator_api = mocker.patch('messaging.services.OperatorAPI')
    operator_api.return_value.send_sms.return_value = mock.Mock(status_code=201)
    repo = mocker.patch('messaging.services.MessageRepository')

    ms = SendMessageService()
    ms.send(sender='21981527318', receiver='21981211250', body='Hello!')

    repo.return_value.create.assert_called_with('21981527318', '21981211250', 'Hello!', None)


def test_should_make_a_request_to_the_operator_api(mocker):
    operator_api = mocker.patch('messaging.services.OperatorAPI')
    operator_api.return_value.send_sms.return_value = mock.Mock(status_code=201)
    repo = mocker.patch('messaging.services.MessageRepository')
    repo.return_value.create.return_value = mock.Mock(id=100)

    ms = SendMessageService()
    ms.send(sender='21981527318', receiver='21981211250', body='Hello!')

    operator_api.return_value.send_sms.assert_called_with(100, '21981527318', '21981211250', 'Hello!')


def test_should_update_status(mocker):
    operator_api = mocker.patch('messaging.services.OperatorAPI')
    operator_api.return_value.send_sms.return_value = mock.Mock(status_code=201)

    repo = mocker.patch('messaging.services.MessageRepository')
    repo.return_value.create.return_value = mock.Mock(id=100)

    ms = SendMessageService()
    ms.send(sender='21981527318', receiver='21981211250', body='Hello!')

    repo.return_value.update_status_code.assert_called_with(100, 201)


# Helpers
# -------------------------------------------------------------------------------------------------

def old_date():
    return datetime.datetime.now() - datetime.timedelta(days=1)
