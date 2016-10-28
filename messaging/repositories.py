from messaging.models import Message


class MessageRepository(object):
    def __init__(self, db):
        self.db = db

    def create(self, sender, receiver, body, expiration_date=None):
        message = Message(sender, receiver, body, expiration_date)
        self.db.session.add(message)
        self.db.session.commit()
        return message

    def update_status_code(self, id, status_code):
        message = Message.query.get(id)
        message.status_code = status_code
        self.db.session.add(message)
        self.db.session.commit()
