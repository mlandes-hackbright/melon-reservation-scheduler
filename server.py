from flask import Flask, render_template, redirect, request, session
import service

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET"])
def login():
    return render_template('login.html')

@app.route("/login", methods=["POST"])
def process_login():
    username = request.form["username"]
    password = request.form["password"]
    app.logger.info(f"login from user {username} with {password}")
    return redirect("/")

@app.route("/schedule")
def schedule():
    return render_template('schedule.html')

@app.route("/results")
def results():
    return render_template('results.html')
