from flask import Blueprint, request, jsonify, session
from app.models import User, Post, Comment, Vote
from app.db import get_db
# facilitates error message display
import sys

# any routes defined within this file will automatically become part of Flask app with prefix of /api
bp = Blueprint('api', __name__, url_prefix='/api')

# USER ROUTES -----------------------------------------
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

# COMMENT ROUTES -----------------------------------------
@bp.route('/comments', methods=['POST'])
def comment():
  data = request.get_json()
  db = get_db()

  try:
    # create a new comment
    newComment = Comment(
      comment_text = data['comment_text'],
      post_id = data['post_id'],
      user_id = session.get('user_id')
    )

    db.add(newComment)
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Comment failed'), 500

  return jsonify(id = newComment.id)

# POST ROUTES ------------------------------------------------
@bp.route('/posts/upvote', methods=['PUT'])
def upvote():
  data = request.get_json()
  db = get_db()

  try:
    # create a new vote with incoming id and session id
    newVote = Vote(
      post_id = data['post_id'],
      user_id = session.get('user_id')
    )

    db.add(newVote)
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Upvote failed'), 500

  return '', 204

@bp.route('/posts', methods=['POST'])
def create():
  data = request.get_json()
  db = get_db()

  try:
    # create a new post
    newPost = Post(
      title = data['title'],
      post_url = data['post_url'],
      user_id = session.get('user_id')
    )

    db.add(newPost)
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Post failed'), 500

  return jsonify(id = newPost.id)

@bp.route('/posts/<id>', methods=['PUT'])
# captures 'id' parameter within 'update' fn and uses it to perform update
def update(id):
  data = request.get_json()
  db = get_db()

  # queries db for corresponding record, updates record and re-commits; NOTE: 'data' variable is a dictionary --> bracket notation and 'post' variable is an object (created from User class) --> dot notation
  try:
    # retrieve post and update title property
    post = db.query(Post).filter(Post.id == id).one()
    post.title = data['title']
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Post not found'), 404

  return '', 204

@bp.route('/posts/<id>', methods=['DELETE'])
def delete(id):
  db = get_db()

  try:
    # delete post from db
    db.delete(db.query(Post).filter(Post.id == id).one())
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Post not found'), 404

  return '', 204