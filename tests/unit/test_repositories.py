from messaging.repositories import MessageRepository
from messaging.models import Message


class TestMessageRepository(object):
    def test_create(self, session):
        repo = MessageRepository()
        msg = repo.create(sender='21981527318', receiver='21980072800', body='Hello World!')

        assert isinstance(msg, Message)
        assert Message.query.get(1) is not None

    def test_update_status_code(self, session):
        msg = Message(sender='21981527318', receiver='21980072800', body='Hello World!')
        session.add(msg)
        session.commit()

        repo = MessageRepository()
        msg = repo.update_status_code(id=1, status_code=201)

        assert msg is None
        assert Message.query.get(1).status_code == 201
