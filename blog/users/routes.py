
from flask import Blueprint

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from blog import db, bcrypt
from blog.models import User, Post
from blog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from blog.users.utils import save_picture, send_reset_email

users = Blueprint("users",__name__) # like creating instance of flask object

# we will not use app anymore we will use users blueprint and later register

@users.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        flash("Already logged in..",category="warning")
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data , email = form.email.data , password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}",category="success")
        return redirect(url_for("login")) # home is the function of the home route

    return render_template("register.html",form=form,title="Register")

@users.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        flash("Already logged in..",category="warning")
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password , form.password.data): # hashed_password in the database and the submiited password
            # logging user using login_user function
            login_user(user=user , remember=form.remember.data)
            """
                Now when user is not logged in and tries to get to a route then it is present in the url as next.
                http://127.0.0.1:5000/login?next=%2F like this.
                So we can grab it to redirect the user where he wants after login
            """
            next_page = request.args.get("next") # next arg may or may not be present
            flash(f"Log in successfull",category="success")
            # ternary conditional
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash(f"Log in Unsuccessfull",category="danger")
    return render_template("login.html",form=form,title="Login")

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@users.route("/account",methods=['GET',"POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            # if picture file present then update the file.
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            db.session.commit()
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Account Updated!","success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        # setting form values to current user data values so that they are filled up on starting automatically
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static",filename=current_user.image_file)
    return render_template("account.html",title="Account", image_file = image_file , form=form)

@users.route("/user/<string:username>")
@login_required
def user_posts(username):
    page = request.args.get("page",default=1 , type=int)
    user = User.query.filter_by(username=username).first_or_404()
    number_of_posts_per_page = 5
    posts = Post.query\
        .filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page,per_page=number_of_posts_per_page)
    
    return render_template("user_posts.html",user=user,post = posts)

@users.route("/reset_password",methods=["GET","POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash("Email has been sent with instructions to reset your email to reset your password")
        return redirect(url_for("login"))
    return render_template("reset_password.html",title="Reset Password",form = form)


@users.route("/reset_password/<token>",methods=["GET","POST"])
def reset_token(token):

    if current_user.is_authenticated:
        return redirect(url_for("home"))
    
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is invalid token or expired token","warning")
        return redirect(url_for("reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashed_password
        db.session.commit()
        flash(f"Password has been updated",category="success")
        return redirect(url_for("login")) # home is the function of the home route

    return render_template("reset_token.html",title="Reset Password",form = form)