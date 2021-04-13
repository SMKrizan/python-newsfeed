from app.db import Base
# we use classes from sqlalchemy module to define data columns and their data types
from sqlalchemy import Column, Integer, String
# 
from sqlalchemy.orm import validates
# 
import bcrypt
salt = bcrypt.gensalt()

# User class inherits from the Base class
class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
#   'nullable=false' in SQL becomes 'NOT NULL'
  username = Column(String(50), nullable=False)
  email = Column(String(50), nullable=False, unique=True)
  password = Column(String(100), nullable=False)

  # this is a 'decorator' that handles this method's request internally (similar to @bp.routes() decorator used for handling route functions)
  @validates('email')
  # 'validate_email' method uses 'assert' keyword to check whether email contains '@' and throws error if false, preventing return statement 
  def validate_email(self, key, email):
    #ensures email address contains '@' character
    assert '@' in email

    return email

  @validates('password')
  def validate_password(self, key, password):
    assert len(password) > 4

    # encrypts password
    return bcrypt.hashpw(password.encode('utf-8'), salt)