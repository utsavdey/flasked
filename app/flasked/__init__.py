from flask import Flask
app = Flask(__name__)
 
app.secret_key = 'your_secret_key'
 
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'your_email_id@gmail.com'
app.config["MAIL_PASSWORD"] = 'Your_password'

from flasked.routes import mail
mail.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/database_name'
from flasked.models import db
db.init_app(app)
