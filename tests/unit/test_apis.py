from flask import current_app
from messaging.apis import send_sms


def test_send_sms(app, mocker):
    #with current_app.test_request_context():
    request = mocker.patch('messaging.apis.request')
    request.content_type = 'application/json'
    message = mocker.patch('messaging.apis.Message')

    send_sms()

    #message.assert_called_with()

