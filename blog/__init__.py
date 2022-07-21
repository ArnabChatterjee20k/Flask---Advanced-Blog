from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os

app = Flask(__name__) # name means name of this module which is main

app.config["SECRET_KEY"] = '761f9d132273fe311f3e13be9faa56b6'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db" # here /// means the relative path which address the folder

db = SQLAlchemy(app)
bcrypt = Bcrypt()
login_manager = LoginManager(app)
# to tell log_manager where our login route is located. Specially required for login_required function
login_manager.login_view = "login" # function name of the login route
login_manager.login_message_category = "info"

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
mail = Mail(app)

# importing blueprints
from blog.users.routes import users
from blog.post.routes import posts
from blog.main.routes import main

# registering imported blueprints
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)