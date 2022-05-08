from flask import Flask

app = Flask(__name__) # name means name of this module which is main

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"