from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
 
db = SQLAlchemy()
 
class User(db.Model):
  __tablename__ = 'users'
  uid = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  email = db.Column(db.String(120), unique=True)
  pwdhash = db.Column(db.String(54))
   
  def __init__(self, firstname, lastname, email, password):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.email = email.lower()
    self.set_password(password)
     
  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)
   
  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)
    
class Article(db.Model):
  __tablename__ = 'articles'
  id = db.Column(db.Integer, primary_key = True)
  title = db.Column(db.String(120))
  
  def __init__(self, title):
    self.title = title.lower()
    
class Finished(db.Model):
  __tablename__ = 'finished'
  id = db.Column(db.Integer, primary_key = True)
  state = db.Column(db.Integer)
  uid= db.Column(db.Integer)
  aid= db.Column(db.Integer)
  def __init__(self, state,uid,aid):
    self.state = state
    self.uid = uid
    self.aid = aid
