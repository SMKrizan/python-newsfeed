from datetime import datetime
from app.db import Base
from .Vote import Vote
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, select, func
from sqlalchemy.orm import relationship, column_property

# SQLAlchemy models are written as Python classes
class Post(Base):
  __tablename__ = 'posts'
  id = Column(Integer, primary_key=True)
  title = Column(String(100), nullable=False)
  post_url = Column(String(100), nullable=False)
#   references users table
  user_id = Column(Integer, ForeignKey('users.id'))
#   when the model is queried,this dynamic property performs a SELECT & with func.count() method adds up votes similar to raw SQL query: (SELECT COUNT(votes.id) AS vote_count FROM votes WHERE votes.post_id = 1;)
  vote_count = column_property(
    select([func.count(Vote.id)]).where(Vote.post_id == id)
  )
#   the following two reference Python's built-in timestamp 
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

#   comes into play with SELECT queries
  user = relationship('User')
    # deletes corresponding foreign key (comment) records when post is deleted; similar to ON DELETE CASCADE in MYSQL
  comments = relationship('Comment', cascade='all,delete')
