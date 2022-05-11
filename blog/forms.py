from flask_wtf import FlaskForm
from flask_wtf.file import FileField , FileAllowed
from flask_login import current_user
from wtforms import StringField , PasswordField , SubmitField , BooleanField , ValidationError
from wtforms.validators import DataRequired , Length , Email , EqualTo
from blog.models import User

class RegistrationForm(FlaskForm):
    """ For user registration form """
    username = StringField("Username",validators=[DataRequired(),Length(min=2,max=20)]) # label and validation
    email = StringField("Email" ,validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    # should be same as password so we will use equalto class
    confirm_password = PasswordField("Confirm Password",validators=[DataRequired(),EqualTo("password")])
    submit = SubmitField("Sign UP")

    """ 
        Here we are using ValidationError class to raise the error and 
        it will be automatically send to the jinja as error attribute 
        and will come down the inputfields.
    """
    
    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already exists...")
    
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already exists...")

class LoginForm(FlaskForm):
    """ For user registration form """
    email = StringField("Email" ,validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    """ For updating account """
    username = StringField("Username",validators=[DataRequired(),Length(min=2,max=20)]) # label and validation
    email = StringField("Email" ,validators=[DataRequired(),Email()])
    picture = FileField("Update Profile Picture",validators=[FileAllowed(["jpg","png"])])
    submit = SubmitField("Update")
    
    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username already exists...")
    
    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Email already exists...")