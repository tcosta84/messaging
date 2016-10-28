import requests


class OperatorAPI(object):
    def send_sms(self, id, sender, receiver, body):
        data = {
            "id": id,
            "from": sender,
            "to": receiver,
            "body": body
        }
        return requests.put('http://localhost:5000/operator/api/v1/sms', json=data)
