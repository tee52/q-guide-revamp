from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

import sqlite3

# configure application
app = Flask(__name__)

# use q-guide database
db = sqlite3.connect("q-guide.db")

@app.route("/")
def home():
    return "Hello world!"
