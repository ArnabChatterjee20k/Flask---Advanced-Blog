from flask import Flask

app = Flask(__name__) # name means name of this module which is main

@app.route("/")
def home():
    return "<p>Hello, World!</p>"

@app.route("/about")
def about():
    return "<p>ABout!</p>"

if __name__ == "__main__":
    app.run(debug=True)