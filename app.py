from flask import Flask,redirect, render_template, url_for

app = Flask(__name__)

#redirect root to /welcome
@app.route("/")
def redirect_page():
    return redirect(url_for("welcome"))


@app.route("/welcome/")
def welcome():
    return render_template("welcome.html")

#return welcome home or welcome back using same template.
@app.route("/welcome/home")
def welcome_home():
    return render_template("_welcome.html", value = "home")

@app.route("/welcome/back")
def welcome_back():
    return render_template("_welcome.html", value = "back")
