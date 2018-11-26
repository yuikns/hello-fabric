import os

# from flask import Flask, request, render_template, redirect
from flask import Flask, render_template, redirect

from .config import FlaskDefaultConfig
from .echo import example
from .extensions import load_extensions

# from .utils import INSTANCE_FOLDER_PATH

MY_BLUEPRINTS = [
    example
]


def create_app(config=None, app_name=None, blueprints=None):
    if app_name is None:
        app_name = FlaskDefaultConfig.PROJECT
    if blueprints is None:
        blueprints = MY_BLUEPRINTS
    if config is None:
        config = FlaskDefaultConfig

    app = Flask(app_name)

    @app.route("/")
    def home():
        return redirect("/example", code=302)

    configure_app(app, config)
    configure_hook(app)
    configure_blueprints(app, blueprints)
    configure_extensions(app)
    configure_logging(app)
    configure_template_filters(app)
    configure_error_handlers(app)
    configure_jinja(app)
    # configure_uploads_handlers(app)

    return app


def configure_app(app, config=None):
    """Different ways of configurations."""

    # http://flask.pocoo.org/docs/api/#configuration
    if config:
        app.config.from_object(config)

    # http://flask.pocoo.org/docs/config/#instance-folders
    app.config.from_pyfile('production.cfg', silent=True)

    # Use instance folder instead of env variables to make deployment easier.
    app.config.from_envvar('%s_APP_CONFIG' % config.PROJECT.upper(), silent=True)


def configure_jinja(app):
    # resolving conflicts between jinja and angular.js
    app.jinja_env.variable_start_string = '{{ '
    app.jinja_env.variable_end_string = ' }}'


def configure_extensions(app):
    load_extensions(app)

def configure_blueprints(app, blueprints):
    """Configure blueprints in views."""

    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def configure_template_filters(app):
    @app.template_filter()
    def pretty_date(value):
        return pretty_date(value)

    @app.template_filter()
    def format_date(value, format='%Y-%m-%d'):
        return value.strftime(format)


def configure_logging(app):
    """Configure file(info) and email(error) logging."""

    if app.debug or app.testing:
        # Skip debug and test mode. Just check standard output.
        return

    import logging
    from logging.handlers import RotatingFileHandler

    # Set info level on logger, which might be overwritten by handers.
    # Suppress DEBUG messages.
    app.logger.setLevel(logging.INFO)

    info_log = os.path.join(app.config['LOG_FOLDER'], 'info.log')
    info_file_handler = RotatingFileHandler(info_log, maxBytes=100000, backupCount=10)
    info_file_handler.setLevel(logging.INFO)
    my_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    info_file_handler.setFormatter(my_formatter)
    app.logger.addHandler(info_file_handler)


def configure_hook(app):
    @app.before_request
    def before_request():
        # filter here
        pass


def configure_error_handlers(app):
    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template("errors/forbidden_page.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/page_not_found.html"), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template("errors/server_error.html"), 500

# def configure_uploads_handlers(app):
#     from .examples.flask.upload.views import pdf_uploads, img_uploads
#     from flask_uploads import configure_uploads
#     configure_uploads(app, (img_uploads, pdf_uploads,))
#     pass
