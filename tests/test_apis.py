import json


def test_should_send(client, session, mocker):
    operator_api_mock = mocker.patch('messaging.apis.OperatorAPI')
    operator_api_mock.return_value.send_sms.return_value.status_code = 201

    data = {'id': 100, 'from': '21981527318', 'to': '21980072800', 'body': 'Hello!'}

    resp = client.put('/api/v1/send_sms', data=json.dumps(data), content_type='application/json')

    assert resp.status_code == 201
    assert resp.json['detail'] == 'Message sent.'


def test_should_not_send_when_message_size_is_greater_than_160_chars(client, session):
    data = {'id': 100, 'from': '21981527318', 'to': '21980072800', 'body': 'a' * 161}

    resp = client.put('/api/v1/send_sms', data=json.dumps(data), content_type='application/json')

    assert resp.status_code == 400
    assert resp.json['error'] == 'Message size is greater than 160 chars.'


def test_should_not_send_when_message_is_already_expired(client, session):
    data = {'id': 100, 'from': '21981527318', 'to': '21980072800', 'body': 'Hello World!', 'expiration_date': '2016-07-14T18:00'}

    resp = client.put('/api/v1/send_sms', data=json.dumps(data), content_type='application/json')

    assert resp.status_code == 400
    assert resp.json['error'] == 'Message is already expired.'


def test_response_when_external_service_responds_with_error_code(client, session, mocker):
    operator_api_mock = mocker.patch('messaging.apis.OperatorAPI')
    operator_api_mock.return_value.send_sms.return_value.status_code = 404

    data = {'id': 100, 'from': '21981527318', 'to': '21980072800', 'body': 'Hello!'}

    resp = client.put('/api/v1/send_sms', data=json.dumps(data), content_type='application/json')

    assert resp.status_code == 200
    assert resp.json['error'] == 'Message not sent. Operator API response: "Mobile User not found"'


def test_should_not_send_when_contenttype_is_not_set_or_is_invalid(client):
    data = {}

    resp = client.put('/api/v1/send_sms', data=json.dumps(data))

    assert resp.status_code == 400
    assert resp.json['error'] == 'Content-type is not valid.'


def test_validation_error(client, session):
    data = {'id': 1}

    resp = client.put('/api/v1/send_sms', data=json.dumps(data), content_type='application/json')

    assert resp.status_code == 400