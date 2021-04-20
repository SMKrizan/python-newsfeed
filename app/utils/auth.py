from flask import session, redirect
# contains several helper functions that can be used to change other fns
from functools import wraps

# redirects a user who isn't logged in OR runs original route fn for logged-in user
def login_required(func):
  @wraps(func)
  def wrapped_function(*args, **kwargs):
    # if logged in, call original function with original arguments
    if session.get('loggedIn') == True:
      return func(*args, **kwargs)

    return redirect('/login')
  
  return wrapped_function