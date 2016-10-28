import pytest

from sqlalchemy_utils.functions import database_exists, create_database, drop_database

from messaging import create_app
from messaging.settings import TestConfig
from messaging.extensions import db as _db


@pytest.yield_fixture(scope='session')
def app():
    _app = create_app(TestConfig)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='session')
def db(app, request):
    url_db_test = app.config['SQLALCHEMY_DATABASE_URI']

    if database_exists(url_db_test):
        drop_database(url_db_test)

    create_database(url_db_test)

    _db.app = app
    _db.create_all()

    def teardown():
        _db.drop_all()
        drop_database(url_db_test)

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture(scope='function')
def client(app, request):
    return app.test_client()
