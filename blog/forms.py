from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField , BooleanField
from wtforms.validators import DataRequired , Length , Email , EqualTo

class RegistrationForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired(),Length(min=2,max=20)]) # label and validation
    email = StringField("Email" ,validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    # should be same as password so we will use equalto class
    confirm_password = PasswordField("Confirm Password",validators=[DataRequired(),EqualTo("password")])
    submit = SubmitField("Sign UP")

class LoginForm(FlaskForm):
    email = StringField("Email" ,validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")