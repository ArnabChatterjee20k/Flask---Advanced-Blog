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

# to avoid the circular imports we will import it after db initialisation
from blog import routes