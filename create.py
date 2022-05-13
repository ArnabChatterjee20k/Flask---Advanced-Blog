from blog.models import db , User , Post
user = User.query.get(1)

for i in range(30):
    post = Post(
        title = "bot scripting",
        content = "a bot created this post",
        author = user
    )
    db.session.add(post)

db.session.commit()