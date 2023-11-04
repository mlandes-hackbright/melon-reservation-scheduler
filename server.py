from flask import Flask, render_template, redirect, request, session, url_for
from datetime import datetime
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
    reservations = service.get_reservations(username)
    
    return render_template("home.html", vm = {
        "username": user.username,
        "reservations": [ r.datetime.strftime("%A, %B %d, %Y @ %I:%M %p") for r in reservations ]
    })

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

@app.route("/schedule", methods=["POST"])
def process_schedule_request():
    if S_USER_KEY not in session:
        return redirect(url_for("index"))
    
    username = session[S_USER_KEY]
    user = service.get_user(username)
    reservations = service.get_reservations(username)
    reservation_times = [r.datetime for r in reservations]
    all_reservation_times = service.get_all_reservation_times()
    
    appointment_time_str = request.form["sdtime"]
    appointment_time = datetime.fromisoformat(appointment_time_str)
    appointment_date_only = appointment_time.replace(hour=0, minute=0, second=0)

    app.logger.info(reservation_times)
    app.logger.info(appointment_time)
    app.logger.info(appointment_date_only)
    app.logger.info(all_reservation_times)
    if appointment_date_only in [t.replace(hour=0, minute=0, second=0) for t in reservation_times]:
        return render_template("results.html", vm = {
            "success": False,
            "message": "you already have an appointment on that date"
        })
    elif appointment_time in all_reservation_times:
        return render_template("results.html", vm = {
            "success": False,
            "message": "somebody else has an appointment at that time already"
        })
    else:
        service.add_reservation(username, appointment_time)
        return render_template("results.html", vm = {
            "success": True
        })

    
