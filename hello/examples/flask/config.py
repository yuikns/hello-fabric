from ...config import DefaultConfig


class FlaskDefaultConfig(DefaultConfig):
    # Flask-babel: http://pythonhosted.org/Flask-Babel/
    ACCEPT_LANGUAGES = ['en']
    BABEL_DEFAULT_LOCALE = 'en'

    # Flask-cache: http://pythonhosted.org/Flask-Cache/
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 60

    # Flask-openid: http://pythonhosted.org/Flask-OpenID/
    # OPENID_FS_STORE_PATH = os.path.join(INSTANCE_FOLDER_PATH, 'openid')
    # mkdirs(OPENID_FS_STORE_PATH)

    # https://pythonhosted.org/Flask-JWT/_modules/flask_jwt.html#verify_jwt
    # JWT
    # 'JWT_DEFAULT_REALM': 'Login Required',
    # 'JWT_AUTH_URL_RULE': '/auth',
    # 'JWT_AUTH_ENDPOINT': 'jwt',
    # 'JWT_ALGORITHM': 'HS256',
    # 'JWT_VERIFY': True,
    # 'JWT_VERIFY_EXPIRATION': True,
    # 'JWT_LEEWAY': 0,
    # 'JWT_EXPIRATION_DELTA': timedelta(seconds=300)
    from datetime import timedelta
    JWT_EXPIRATION_DELTA = timedelta(days=30)

    # for upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
