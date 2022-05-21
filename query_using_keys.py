from blog.models import Post , User
from blog import db

def get_post(author="arnab",per_page=5):
    #TODO: to query the post table using a author first page only. A case of pagination
    username = author
    user = User.query.filter_by(username=username).first_or_404()
    number_of_posts_per_page = per_page
    # \ is used to break a query into multiple lines
    posts = Post.query\
        .filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=1,per_page=number_of_posts_per_page) # author is the backref in user to communicate with post
    
    for author_post in posts.items:
        print(f"{author_post} ->  {posts.per_page}")

get_post()