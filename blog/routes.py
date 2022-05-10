from flask import flash, redirect , render_template , url_for
from blog import app , db , bcrypt
# as forms and models are a part of the blog package now
from blog.forms import RegistrationForm , LoginForm
from blog.models import User , Post
from flask_login import login_user , current_user , logout_user , login_required

posts = [
    {
        "author":"Arnab",
        "title" : "Blog post",
        "content" : "First",
        "date" : "sldkjfl"
    },
    {
        "author":"Arnab",
        "title" : "Blog post",
        "content" : "First",
        "date" : "sldkjfl"
    },
    {
        "author":"Arnab",
        "title" : "Blog post",
        "content" : "First",
        "date" : "sldkjfl"
    },
    {
        "author":"Arnab",
        "title" : "Blog post",
        "content" : "First",
        "date" : "sldkjfl"
    },
    {
        "author":"Arnab",
        "title" : "Blog post",
        "content" : "First",
        "date" : "sldkjfl"
    },
]

@app.route("/")
@login_required
def home():
    return render_template("home.html",post = posts)

@app.route("/about")
def about():
    return render_template("about.html",title="about")

@app.route("/register",methods=['GET','POST'])
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

@app.route("/login",methods=['GET','POST'])
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
            flash(f"Log in successfull",category="success")
            return redirect(url_for("home"))
        else:
            flash(f"Log in Unsuccessfull",category="danger")
    return render_template("login.html",form=form,title="Login")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/account")
@login_required
def account():
    return render_template("account.html",title="Account")