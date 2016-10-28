from messaging.domains import Message
from messaging.repositories import MessageRepository
from messaging.apiclients import OperatorAPI


class MessageTooLargeError(Exception):
    pass


class ExpiredMessageError(Exception):
    pass


class OperatorAPIError(Exception):
    def __init__(self, status_code):
        self.status_code = status_code


class SendMessageService(object):
    def send(self, sender, receiver, body, expiration_date=None):
        domain = Message(sender, receiver, body, expiration_date)
        if domain.is_large():
            raise MessageTooLargeError()

        if domain.is_expired():
            raise ExpiredMessageError()

        repo = MessageRepository()
        message = repo.create(sender, receiver, body, expiration_date)

        apiclient = OperatorAPI()
        resp = apiclient.send_sms(message.id, sender, receiver, body)

        repo.update_status_code(message.id, resp.status_code)

        if resp.status_code != 201:
            raise OperatorAPIError(resp.status_code)
