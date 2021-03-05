from flask import Flask
from app.routes import home, dashboard

# "def" keyword defines the "create_app()" function, which is identified with indentation (2 spaces)
def create_app(test_config=None):
  # set up app config; any static resources will be served from the root directory (and not from the default "static" directory)
  app = Flask(__name__, static_url_path='/')
#   trailing slashes are optional
  app.url_map.strict_slashes = False
#   used when creating server-side sessions
  app.config.from_mapping(
    SECRET_KEY='super_secret_key'
  )

# creates a route to return a message-string
  @app.route('/hello')
  def hello():
      return "hello world"

  # register routes
  app.register_blueprint(home)
  app.register_blueprint(dashboard)

  return app