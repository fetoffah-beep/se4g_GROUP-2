from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager



app = Flask(__name__)
app.config['SECRET_KEY'] = '497f5e863942d4fd0a245f1226934286'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
db.create_all()
login_manager = LoginManager(app)
login_manager.login_view = 'login' ## passing the url
login_manager.login_message_category = 'info'

from flaskblog import routes

#sqlite:///site.db
#postgresql://postgres:nateriver1994@localhost/PLOS