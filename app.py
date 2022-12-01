from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required

import sqlite3

# configure application
app = Flask(__name__)
app.run

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# use q-guide database
connection = sqlite3.connect("q-guide.db", check_same_thread=False)
db = connection.cursor()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=['GET', 'POST'])
def start():
    if session.get("user_id") is None:
        if request.method == 'POST':
            return redirect("/login")
        else:
            return render_template("start.html")
    
    else:
        return render_template("home.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    """log user in"""

    # forget current user id, if any
    session.clear()

    if request.method == "POST":
        # check if username was entered
        if not request.form.get("username"):
            return render_template("login.html", error="must enter username")

        # check if password was entered
        elif not request.form.get("password"):
            return render_template("login.html", error="must enter password")

        # search database for username
        db.execute("SELECT * FROM users WHERE username = (?)", (request.form.get("username"),))
        rows = db.fetchall()

        # check if username is in database and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            return render_template("login.html", error="invalid username and/or password")

        # remember which user is logged in
        session["user_id"] = rows[0][0]

        # redirect to home page (login required)
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    """register user"""

    if request.method == "POST":
        db.execute("SELECT username FROM users")
        usernames = db.fetchall()

        # check if username was entered
        if not request.form.get("username"):
            return render_template("register.html", error="must enter username")

        # check if password was entered
        elif not request.form.get("password") or not request.form.get("confirmation"):
            return render_template("register.html", error="must enter password")

        # check if username is already in database
        elif request.form.get("username") in usernames:
            return render_template("register.html", error="username is not unique")

        elif request.form.get("confirmation") != request.form.get("password"):
            return render_template("register.html", error="passwords do not match")

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (request.form.get("username"), generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)))
        connection.commit()

        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    """log user out"""

    # forget any user_id
    session.clear()

    # redirect user to start screen
    return redirect("/")
