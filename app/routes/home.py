from flask import Blueprint, render_template, session, redirect
from app.models import Post
from app.db import get_db

# consolidates routes into a single "bp" object (similar to using "Router" middleware in Express.js)
bp = Blueprint('home', __name__, url_prefix='/')

# returns session-connection tied to this route's context and queries Post model for all posts in descending order
@bp.route('/')
def index():
  # get all posts
  db = get_db()
  # compare the following line to the equivalent statement in dashboard.py to see alt formatting example
  posts = db.query(Post).order_by(Post.created_at.desc()).all()
  return render_template(
    'homepage.html',
    posts=posts,
    loggedIn=session.get('loggedIn')
  )

@bp.route('/login')
def login():
  # not logged in yet
  if session.get('loggedIn') is None:
    return render_template('login.html')

  return redirect('/dashboard')
  
# route parameter <id> within decorator function becomes a function parameter within single() fn, which can be used to query db for a specific post
@bp.route('/post/<id>')
def single(id):
  # get single post by id using filter() to specify SQL WHERE clause, ending with one() instead of all()
  db = get_db()
  post = db.query(Post).filter(Post.id == id).one()

  # single post object is passed to single post template for rendering
  return render_template(
    'single-post.html',
    post=post,
    loggedIn=session.get('loggedIn')
  )