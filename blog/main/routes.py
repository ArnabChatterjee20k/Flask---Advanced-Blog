from flask import render_template, request, Blueprint
from blog.models import Post
from flask import Blueprint
main = Blueprint("main",__name__)

@main.route("/")
def home():
    page = request.args.get("page",default=1 , type=int)
    number_of_posts_per_page = 5
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=number_of_posts_per_page)
    return render_template("home.html",post = posts)

@main.route("/about")
def about():
    return render_template("about.html",title="about")

