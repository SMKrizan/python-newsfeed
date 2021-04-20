# directs program to find 'home' module and import 'bp' object, renaming it as 'home'
from .home import bp as home

from .dashboard import bp as dashboard

# uses Flask app to register blueprint
from .api import bp as api