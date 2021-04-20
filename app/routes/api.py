from flask import Blueprint, request, jsonify, session
from app.models import User
from app.db import get_db
# facilitates error message display
import sys

# any routes defined within this file will automatically become part of Flask app with prefix of /api
bp = Blueprint('api', __name__, url_prefix='/api')

# POST route will resolve to '/api/users' and uses the imported 'request' object which contains information about requests
@bp.route('/users', methods=['POST'])
def signup():
  data = request.get_json()
  db = get_db()

  try:
  # attempts to create a new user; note the use of brackets (instead of dot-notation) for defining the data 'dictionary' (as opposed to obect)
    newUser = User(
      username=data['username'],
      email=data['email'],
      password=data['password']
    )

  # save in database; 'add' method --> preps 'INSERT' statement and 'commit' method --> updates db
    db.add(newUser)
    db.commit()
  except:
    # should throw 'AssertionError' if custom validations fail and 'IntegrityError' with MySQL-related errors
    print(sys.exc_info()[0])
    # insert failed, so rollback (esures db will not lock up once deployed) and send error to front end
    db.rollback()
    return jsonify(message='Signup failed'), 500

  # clears any existing session data and creates 'user_id' session ppty to aid future db queries and boolean ppty that templates will use to conditionally render elements
  session.clear()
  session['user_id'] = newUser.id
  session['loggedIn'] = True

  return jsonify(id=newUser.id)

@bp.route('/users/logout', methods=['POST'])
def logout():
  # remove session variables
  session.clear()
  return '', 204

@bp.route('/users/login', methods=['POST'])
def login():
  data = request.get_json()
  db = get_db()

  try:
    user = db.query(User).filter(User.email == data['email']).one()
  except:
    print(sys.exc_info()[0])
    return jsonify(message = 'Incorrect credentials'), 400

  if user.verify_password(data['password']) == False:
    return jsonify(message = 'Incorrect credentials'), 400

  session.clear()
  session['user_id'] = user.id
  session['loggedIn'] = True

  return jsonify(id = user.id)
