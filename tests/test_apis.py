import json

from messaging.services import OperatorAPIError


def test_should_send(client, session, mocker):
    mocker.patch('messaging.apis.SendMessageService')
    data = {'from': '21981527318', 'to': '21980072800', 'body': 'Hello!'}

    resp = client.put('/api/v1/send_sms', data=json.dumps(data), content_type='application/json')

    assert resp.status_code == 201
    assert resp.json['detail'] == 'Message sent.'


def test_should_not_send_when_message_size_is_greater_than_160_chars(client, session):
    data = {'from': '21981527318', 'to': '21980072800', 'body': 'a' * 161}

    resp = client.put('/api/v1/send_sms', data=json.dumps(data), content_type='application/json')

    assert resp.status_code == 400
    assert resp.json['error'] == 'Message size is greater than 160 chars.'


def test_should_not_send_when_message_is_already_expired(client, session):
    data = {'from': '21981527318', 'to': '21980072800', 'body': 'Hello World!', 'expiration_date': '2016-07-14T18:00'}

    resp = client.put('/api/v1/send_sms', data=json.dumps(data), content_type='application/json')

    assert resp.status_code == 400
    assert resp.json['error'] == 'Message is already expired.'


def test_response_when_external_service_responds_with_error_code(client, session, mocker):
    service = mocker.patch('messaging.apis.SendMessageService')
    service.return_value.send.side_effect = OperatorAPIError(status_code=404)

    data = {'from': '21981527318', 'to': '21980072800', 'body': 'Hello!'}

    resp = client.put('/api/v1/send_sms', data=json.dumps(data), content_type='application/json')

    assert resp.status_code == 200
    assert resp.json['error'] == 'Message not sent. Operator API response: "Mobile User not found"'


def test_should_not_send_when_contenttype_is_not_set_or_is_invalid(client):
    data = {}

    resp = client.put('/api/v1/send_sms', data=json.dumps(data))

    assert resp.status_code == 400
    assert resp.json['error'] == 'Content-type is not valid.'


def test_should_not_send_when_json_is_invalid(client, session):
    data = ''

    resp = client.put('/api/v1/send_sms', data=data, content_type='application/json')

    assert resp.status_code == 400
    assert resp.json['error'] == 'Invalid JSON.'


def test_should_not_send_when_request_has_validation_errors(client, session):
    data = {'id': 1}

    resp = client.put('/api/v1/send_sms', data=json.dumps(data), content_type='application/json')

    assert resp.status_code == 400
