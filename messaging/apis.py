from marshmallow import Schema, fields

from werkzeug.exceptions import BadRequest
from flask import Blueprint, jsonify, request

from messaging.services import SendMessageService, MessageTooLargeError, ExpiredMessageError, OperatorAPIError

blueprint = Blueprint('api', __name__)


class ApiSchema(Schema):
    sender = fields.String(load_from='from', required=True)
    receiver = fields.String(load_from='to', required=True)
    body = fields.String(required=True)
    expiration_date = fields.DateTime('%Y-%m-%dT%H:%M')


@blueprint.route('/api/v1/send_sms', methods=['PUT'])
def send_sms():
    if request.content_type != 'application/json':
        return jsonify(error='Content-type is not valid.'), 400

    try:
        data = request.json
    except BadRequest:
        return jsonify(error='Invalid JSON.'), 400

    schema = ApiSchema()
    res = schema.load(data)
    if res.errors:
        return jsonify(errors=res.errors), 400

    sender = res.data.get('sender')
    receiver = res.data.get('receiver')
    body = res.data.get('body')
    expiration_date = res.data.get('expiration_date')

    try:
        ms = SendMessageService()
        ms.send(sender, receiver, body, expiration_date)
    except MessageTooLargeError as e:
        return jsonify(error='Message size is greater than 160 chars.'), 400
    except ExpiredMessageError as e:
        return jsonify(error='Message is already expired.'), 400
    except OperatorAPIError as e:
        api_resp = {
            201: 'Sms sent',
            404: 'Mobile User not found',
            405: 'Validation exception',
            500: 'Internal Server Error'
        }
        error_msg = 'Message not sent. Operator API response: "{0}"'.format(api_resp[e.status_code])
        return jsonify(error=error_msg), 200

    return jsonify(detail='Message sent.'), 201


@blueprint.route('/operator/api/v1/sms', methods=['PUT'])
def fake_operator_api():
    sender = request.json.get('from')
    receiver = request.json.get('to')

    known_numbers = ['21981527318', '21980072800']
    if sender not in known_numbers or receiver not in known_numbers:
        return jsonify(description='Mobile User not found'), 404

    return jsonify(description='Sms sent'), 201
