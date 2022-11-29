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

    if request.method == "POST":
        return redirect("/home")
    else:
        return render_template("login.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        return redirect("/home")

    else:
        return render_template("register.html")
