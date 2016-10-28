import datetime


class Message(object):
    def __init__(self, sender, receiver, body, expiration_date=None):
        self.sender = sender
        self.receiver = receiver
        self.body = body
        self.expiration_date = expiration_date

    def is_large(self):
        return len(self.body) > 160

    def is_expired(self):
        return self.expiration_date and self.expiration_date <= datetime.datetime.now()
