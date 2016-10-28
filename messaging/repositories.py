from messaging.models import Message
from messaging.extensions import db


class MessageRepository(object):
    def create(self, sender, receiver, body, expiration_date=None):
        message = Message(sender, receiver, body, expiration_date)
        db.session.add(message)
        db.session.commit()
        return message

    def update_status_code(self, id, status_code):
        message = Message.query.get(id)
        message.status_code = status_code
        db.session.add(message)
        db.session.commit()
