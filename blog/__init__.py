from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__) # name means name of this module which is main

app.config["SECRET_KEY"] = '761f9d132273fe311f3e13be9faa56b6'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db" # here /// means the relative path which address the folder

db = SQLAlchemy(app)
bcrypt = Bcrypt()
login_manager = LoginManager(app)
# to tell log_manager where our login route is located. Specially required for login_required function
login_manager.login_view = "login" # function name of the login route
login_manager.login_message_category = "info"

# to avoid the circular imports we will import it after db initialisation
from blog import routes