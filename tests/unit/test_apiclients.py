from messaging.apiclients import OperatorAPI


class TestOperatorAPI(object):
    def test_send_sms(self, mocker):
        requests = mocker.patch('messaging.apiclients.requests')

        operator_api = OperatorAPI()
        operator_api.send_sms(100, '21981527318', '21980072800', 'Hello')

        expected_data = {
            "id": 100,
            "from": '21981527318',
            "to": '21980072800',
            "body": 'Hello'
        }

        requests.put.assert_called_with('http://localhost:5000/operator/api/v1/sms', json=expected_data)
