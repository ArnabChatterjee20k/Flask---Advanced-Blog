from flask import Blueprint
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from blog import db
from blog.models import Post
from blog.post.forms import PostForm


posts = Blueprint("posts",__name__)



@posts.route("/post/new",methods=["GET","POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data , 
                    content = form.content.data , 
                    author = current_user) # author is the backref in the user table which links to all data in post. 
                                           # here author is declared to current user means all the details.
        db.session.add(post)
        db.session.commit()
        flash("Post created","success")
        return redirect(url_for("home"))
    return render_template("create_post.html", form = form ,
                            title="New post" , 
                            legend="New Post"
                            )

@posts.route("/post/<int:post_id>",methods=["GET","POST"])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html",title=post.title,post=post)

@posts.route("/post/<int:post_id>/update",methods=["GET","POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        # updating the post
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Post udpated","success")
        return redirect(url_for("home"))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html", form = form ,
                            title="Update post" , 
                            legend = "Update post")

@posts.route("/post/<int:post_id>/delete",methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted","warning")
    return redirect(url_for("home"))

