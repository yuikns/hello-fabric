# -*- coding: utf-8 -*-

from flask_script import Manager

from hello.config import DefaultConfig
from hello.examples.flask.app import create_app

app = create_app()
manager = Manager(app)

@manager.command
def run():
    """Run in local machine."""
    app.run(host=DefaultConfig.FLASK_HOST, port=DefaultConfig.FLASK_PORT, threaded=DefaultConfig.FLASK_THREADED)

@manager.command
def help():
    """Help"""
    print("hello, world!")


manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")

if __name__ == "__main__":
    manager.run()
