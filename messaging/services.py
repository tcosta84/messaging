import datetime
from messaging.domains import Message


class MessageTooLargeError(Exception):
    pass


class ExpiredMessageError(Exception):
    pass


class MessageNotSentError(Exception):
    pass


class SendMessageService(object):
    def __init__(self, MessageRepository, MessageSender):
        self.r = MessageRepository
        self.m = MessageSender

    def send(self, id, sender, receiver, body, expiration_date=None):
        """
        :raises MessageTooLargeError, ExpiredMessageError, MessageNotSentError
        """

        msg = Message(sender, receiver, body, expiration_date)
        if msg.is_large():
            raise MessageTooLargeError()

        if msg.is_expired():
            raise ExpiredMessageError()

        message = self.r.create(sender, receiver, body, expiration_date)

        resp = self.m.send(id, sender, receiver, body)

        self.r.update_status(message.id, resp.status_code)

    def _request(self):
        pass
