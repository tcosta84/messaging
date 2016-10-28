from flask import Flask

from messaging.settings import Config
from messaging.extensions import db, migrate
from messaging.apis import blueprint


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(blueprint)
    return app
