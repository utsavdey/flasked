from flask.ext.wtf import Form
from wtforms.fields import TextField, TextAreaField, SubmitField,PasswordField
from wtforms.validators import DataRequired,Email
from flasked.models import db, User 
 
class ContactForm(Form):
  name = TextField("Name",  validators=[DataRequired("Please enter your name.")])
  email = TextField("Email",  validators=[DataRequired("Please enter your email."), Email("Please enter your email address.")])
  subject = TextField("Subject",  validators=[DataRequired("Please enter your subject.")])
  message = TextAreaField("Message",  validators=[DataRequired("Please enter your message.")])
  submit = SubmitField("Send")
  
class SignupForm(Form):
  firstname = TextField("First name", validators=[DataRequired("Please enter your name.")])
  lastname = TextField("Last name",  validators=[DataRequired("Please enter your last name.")])
  email = TextField("Email",  validators=[DataRequired("Please enter your email."), Email("Please enter your email address.")])
  password = PasswordField('Password', validators=[DataRequired("Please enter your password.")])
  submit = SubmitField("Create account")
 
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user:
      self.email.errors.append("That email is already taken")
      return False
    else:
      return True

class SigninForm(Form):
  email = TextField("Email",  validators=[DataRequired("Please enter your email."), Email("Please enter your email address.")])
  password = PasswordField('Password', validators=[DataRequired("Please enter your password.")])
  submit = SubmitField("Sign In")
   
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user and user.check_password(self.password.data):
      return True
    else:
      self.email.errors.append("Invalid e-mail or password")
      return False
      
class ChangePasswordForm(Form):
  email = TextField("Email",  validators=[DataRequired("Please enter your email."), Email("Please enter your email address.")])
  password = PasswordField('Password', validators=[DataRequired("Please enter your password.")])
  newpassword = PasswordField('New Password', validators=[DataRequired("Please enter your password.")])
  submit = SubmitField("Change")
   
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user and user.check_password(self.password.data):
      return True
    else:
      self.email.errors.append("Invalid e-mail or password")
      return False
	  
class DoneForm(Form):
  submit = SubmitField("Mark")
  
class UndoDoneForm(Form):
  submit = SubmitField("Unmark")    
