from __main__ import db
from datetime import datetime
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
