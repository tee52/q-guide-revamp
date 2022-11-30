from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required

import sqlite3

# configure application
app = Flask(__name__)

# use q-guide database
db = sqlite3.connect("q-guide.db")

@app.route("/", methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        return redirect("/login")
    else:
        return render_template("start.html")


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # check if username is in database and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", error="invalid username and/or password")

        # remember which user is logged in
        session["user_id"] = rows[0]["id"]

        # redirect to home page (login required)
        return redirect("/home")

    else:
        return render_template("login.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    """register user"""

    if request.method == "POST":
        usernames = db.execute("SELECT username FROM users")

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

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8))

        return redirect("/home")

    else:
        return render_template("register.html")


@app.route("/home")
@login_required
def home():
    return render_template("home.html")
