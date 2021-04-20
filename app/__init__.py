from flask import Flask
# able to import 'home' directly from 'routes' because it is called and (re)named in its __init__.py
from app.routes import home, dashboard, api
from app.db import init_db
from app.utils import filters

# "def" keyword defines the "create_app()" function, which is identified with indentation (2 spaces)
def create_app(test_config=None):
# set up app config; any static resources will be served from the root directory (and not from the default "static" directory)
  app = Flask(__name__, static_url_path='/')
# trailing slashes are optional
  app.url_map.strict_slashes = False
# used when creating server-side sessions
  app.config.from_mapping(
    SECRET_KEY='super_secret_key'
  )
# completes registration with Jinja template environment
  app.jinja_env.filters['format_url'] = filters.format_url
  app.jinja_env.filters['format_date'] = filters.format_date
  app.jinja_env.filters['format_plural'] = filters.format_plural
# registers blueprint
  app.register_blueprint(api)

# creates a route to return a message-string
  @app.route('/hello')
  def hello():
      return "hello world"

  # register routes
  app.register_blueprint(home)
  app.register_blueprint(dashboard)

  # initializes db following Flask set-up
  init_db(app)

  return app