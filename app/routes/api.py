from flask import Blueprint, request, jsonify
from app.models import User
from app.db import get_db

# any routes defined within this file will automatically become part of Flask app with prefix of /api
bp = Blueprint('api', __name__, url_prefix='/api')

# POST route will resolve to '/api/users' and uses the imported 'request' object which contains information about requests
@bp.route('/users', methods=['POST'])
def signup():
  data = request.get_json()
  db = get_db()

  # create a new user; note the use of brackets (instead of dot-notation) for defining the data 'dictionary' (as opposed to obect)
  newUser = User(
    username = data['username'],
    email = data['email'],
    password = data['password']
  )

  # save in database; preps 'INSERT' statement and updates db
  db.add(newUser)
  db.commit()

  return jsonify(id = newUser.id)