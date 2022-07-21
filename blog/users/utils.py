import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from blog import app, mail

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

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request",
                    sender="noreply@demo.com",
                    recipients=[user.email])
    msg.body = f"""
                    To reset your password , visit the following the link:-
                    {url_for("reset_token",token=token,_external=True)}
                """ #_external for absolute path

    mail.send(msg)
    return
