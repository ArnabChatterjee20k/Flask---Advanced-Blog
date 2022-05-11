import secrets , os
from PIL import Image
from flask import flash, redirect , render_template , url_for , request
from blog import app , db , bcrypt
# as forms and models are a part of the blog package now
from blog.forms import RegistrationForm , LoginForm , UpdateAccountForm
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

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


def save_picture(form_picture):
    """ For saving the picture into the file and randomising the name of the picture data """
    random_hex= secrets.token_hex(8)
    """ 
        splitting the filename using os module to get the file extension
        then join it with root path of our app using app.root_path and os.path.join
    """
    _ , f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext # new randomised name of the picture
    picture_path = os.path.join(app.root_path , "static/" , picture_fn) # getting the full path

    # resizing the Picture
    output_size = (125,125)
    image = Image.open(form_picture)
    image.thumbnail(output_size)

    image.save(picture_path) # saving our resized picture

    return picture_fn

@app.route("/account",methods=['GET',"POST"])
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