import datetime
from messaging.extensions import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(11), nullable=False)
    receiver = db.Column(db.String(11), nullable=False)
    body = db.Column(db.Text, nullable=False)
    expiration_date = db.Column(db.DateTime)
    status_code = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime)

    def __init__(self, sender, receiver, body, expiration_date=None):
        self.sender = sender
        self.receiver = receiver
        self.body = body
        self.expiration_date = expiration_date

    def __repr__(self):
        return 'From: {0}, To: {1}, Message: {2}'.format(self.sender, self.receiver, self.body)
