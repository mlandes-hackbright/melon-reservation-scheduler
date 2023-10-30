from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/schedule")
def schedule():
    return render_template('schedule.html')

@app.route("/results")
def results():
    return render_template('results.html')
