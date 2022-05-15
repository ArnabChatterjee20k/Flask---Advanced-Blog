from blog.models import db , User , Post
from blog.routes import post
def basics_concept():
    post = Post.query.paginate()
    # 'Pagination' object is not iterable
    # for i in post:
    #     print(i)

    print(dir(post))

    print("Total posts = ",post.total)
    print("Items per page =",post.per_page)
    print("Page =",post.page)

    # getting items of post of 1st page(which is default)
    print("page 1")
    for item in post.items:
        print(item)

    # getting items of post of 2nd page
    post_2 = Post.query.paginate(page=2)
    print("Page 2")
    for item in post_2.items:
        print(item)
    
def setting_per_page():
    post = Post.query.paginate(per_page=5)
    print("Items per page =",post.per_page)
    print("Page =",post.page)
    for item in post.items:
        print(item)

def setting_both():
    # setting page and per_page
    post = Post.query.paginate(per_page=5,page=2)
    print("Page =",post.page)
    for item in post.items:
        print(item)

def get_navigate_pages():
    # getting page numbers
    post = Post.query.paginate(per_page=2,page=2)
    for page in post.iter_pages():
        print(page) # None value representing to the

get_navigate_pages()