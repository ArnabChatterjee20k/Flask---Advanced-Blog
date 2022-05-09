from flask import Flask, flash, redirect , render_template , url_for
from forms import RegistrationForm , LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__) # name means name of this module which is main

app.config["SECRET_KEY"] = '761f9d132273fe311f3e13be9faa56b6'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db" # here /// means the relative path which address the folder

db = SQLAlchemy(app)

# One to Many relationship from User to Post as an User can have many posts
# In User we are referencing the Post class so capital Post
# In post table we are referencing user table so in small letter user.id
class User(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(20),unique=True,nullable=False)
    image_file = db.Column(db.String(20),nullable=False , default="default.jpg") # not unique as all of them will have default image
    password = db.Column(db.String(60),nullable=False)
    # this posts is not a column but an additional query running in the post table to get the post of the user
    posts = db.relationship("Post",backref="author",lazy=True)
    # we can use author in the post table to get the user data
    # also we can use user.posts to get the user posts

    def __repr__(self) :
        return f"User {self.username} , {self.email} , {self.image_file}"

class Post(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    title = db.Column(db.String(120),nullable=False)
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    content = db.Column(db.Text,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    
    def __repr__(self) :
        return f"User {self.title} , {self.date_posted}"


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

if __name__ == "__main__":
    app.run(debug=True)