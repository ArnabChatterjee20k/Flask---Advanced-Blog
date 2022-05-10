from flask import flash, redirect , render_template , url_for
from blog import app
# as forms and models are a part of the blog package now
from blog.forms import RegistrationForm , LoginForm
from blog.models import User , Post

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
def home():
    return render_template("home.html",post = posts)

@app.route("/about")
def about():
    return render_template("about.html",title="about")

@app.route("/register",methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}",category="success")
        return redirect(url_for("home")) # home is the function of the home route

    return render_template("register.html",form=form,title="Register")

@app.route("/login",methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data=="arnabchatterjee.ac@gmail.com" and form.password.data=="1234":
            flash(f"Logged in as {form.email.data}",category="success")
            return redirect(url_for("home"))
        else:
            flash(f"Log in Unsuccessfull",category="danger")
    return render_template("login.html",form=form,title="Login")
