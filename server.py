from flask import Flask, render_template, redirect, request, session, url_for
import service
import os
import sys

ENV_SESSION_KEY = "FLASK_SESSION_ENCRYPTION_KEY"
S_USER_KEY = "SESSION_USER"

app = Flask(__name__)

if ENV_SESSION_KEY not in os.environ:
    app.logger.fatal("missing session encryption key")
    sys.exit()
app.secret_key = os.environ.get(ENV_SESSION_KEY)

@app.context_processor
def inject_user():
    return {
        "logged_in": S_USER_KEY in session
    }

@app.route("/")
def index():
    if S_USER_KEY in session:
        return redirect(url_for("home"))
    
    return render_template('index.html')

@app.route("/home")
def home():
    if S_USER_KEY not in session:
        return redirect(url_for("index"))
    username = session[S_USER_KEY]
    user = service.get_user(username)
    
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/logout")
def logout():
    session.pop(S_USER_KEY)
    return redirect(url_for("index"))

@app.route("/login", methods=["POST"])
def process_login():
    username = request.form["username"]
    password = request.form["password"]

    user = service.get_user(username)
    if user:
        if user.credential.check_password(password):
            app.logger.info(f"login success for {user.username}")
            session[S_USER_KEY] = user.username
            return redirect(url_for("home"))
        else:
            app.logger.warning(f"login failed")
    else:
        app.logger.warning(f"user {username} not found")

    return redirect(url_for("login"))

@app.route("/schedule")
def schedule():
    if S_USER_KEY not in session:
        return redirect(url_for("index"))
    
    return render_template('schedule.html')

@app.route("/results")
def results():
    if S_USER_KEY not in session:
        return redirect(url_for("index"))
    
    return render_template('results.html')
