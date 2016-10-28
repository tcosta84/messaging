#!/usr/bin/env python

from flask_script import Manager, Server
from flask_migrate import MigrateCommand

from messaging import create_app

app = create_app()

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(threaded=True, host='0.0.0.0'))

if __name__ == '__main__':
    manager.run()
