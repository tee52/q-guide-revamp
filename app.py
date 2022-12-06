from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required

import sqlite3

# configure application
app = Flask(__name__, static_url_path='/static')
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
    # if user isn't logged in, go to general start page
    if session.get("user_id") is None:
        return render_template("start.html")
    
    # if user is logged in, go to home page
    else:
        db.execute("SELECT username FROM users WHERE id = (?)", (session["user_id"],))
        username = db.fetchall()

        db.execute("SELECT DISTINCT * FROM courses INNER JOIN scores ON scores.course_id = courses.id ORDER BY RANDOM() LIMIT 3")
        course_recs = db.fetchall()

        return render_template("home.html", username=username[0][0], course_recs=course_recs)


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
        # retrieve all usernames
        db.execute("SELECT username FROM users")
        usernames = db.fetchall()

        # check if username was entered
        if not request.form.get("username"):
            return render_template("register.html", error="must enter username")

        # check if password was entered
        elif not request.form.get("password") or not request.form.get("confirmation"):
            return render_template("register.html", error="must enter password")

        # check if username is already in database
        elif (any(request.form.get("username") in u for u in usernames)):
            return render_template("register.html", error="username is not unique")

        # check if passwords match
        elif request.form.get("confirmation") != request.form.get("password"):
            return render_template("register.html", error="passwords do not match")

        # add user info to users table
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (request.form.get("username"), generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)))
        connection.commit()

        # redirect user to login with their information
        return redirect("/login")

    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    """log user out"""

    # forget any user_id
    session.clear()

    # redirect user to start screen
    return redirect("/")


@app.route("/profile", methods=['GET','POST'])
@login_required
def profile():
    """show user profile"""

    # get user's username
    db.execute("SELECT username FROM users WHERE id = (?)", (session["user_id"],))
    username = db.fetchall()

    # get all usernames
    db.execute("SELECT username FROM users")
    usernames = db.fetchall()

    # get graduation year of user
    db.execute("SELECT grad_year FROM users WHERE id = (?)", (session["user_id"],))
    grad_year = db.fetchall()
            
    # get class of user
    db.execute("SELECT class FROM users WHERE id = (?)", (session["user_id"],))
    curr_class = db.fetchall()

    # get concentration of user
    db.execute("SELECT concentration FROM users WHERE id = (?)", (session["user_id"],))
    concentration = db.fetchall()

    if request.method == "POST":
        # check if the user clicked the button that saves a new username
        if request.form.get("action") == "change_user":
            # check if username was entered
            if not request.form.get("username"):
                return render_template("profile.html", error="must enter new username", username=username[0][0], grad_year=grad_year[0][0], curr_class=curr_class[0][0], concentration=concentration[0][0])

            # check if password was entered
            elif not request.form.get("password"):
                return render_template("profile.html", error="must enter password", username=username[0][0], grad_year=grad_year[0][0], curr_class=curr_class[0][0], concentration=concentration[0][0])

            # check if username is already in database
            elif (any(request.form.get("username") in u for u in usernames)):
                return render_template("profile.html", error="username is already taken", username=username[0][0], grad_year=grad_year[0][0], curr_class=curr_class[0][0], concentration=concentration[0][0])

            # search database for password
            db.execute("SELECT hash FROM users WHERE id = (?)", (session["user_id"],))
            password = db.fetchall()

            # check if password is correct
            if not check_password_hash(password[0][0], request.form.get("password")):
                return render_template("profile.html", error="invalid password", username=username[0][0], grad_year=grad_year[0][0], curr_class=curr_class[0][0], concentration=concentration[0][0])

            # update users table with new username
            db.execute("UPDATE users SET username = (?) WHERE id = (?)", (request.form.get("username"), session["user_id"]))
            connection.commit()

            # retrieve new username
            db.execute("SELECT username FROM users WHERE id = (?)", (session["user_id"],))
            username = db.fetchall()

            return render_template("profile.html", username=username[0][0], grad_year=grad_year[0][0], curr_class=curr_class[0][0], concentration=concentration[0][0])

        # check if the user clicked the button that saves a new password
        elif request.form.get("action") == "change_pass":
            # check if password was entered
            if not request.form.get("current_password"):
                return render_template("profile.html", error="must enter current password", username=username[0][0], grad_year=grad_year[0][0], curr_class=curr_class[0][0], concentration=concentration[0][0])

            # check if password was entered
            elif not request.form.get("new_password") or not request.form.get("new_password2"):
                return render_template("profile.html", error="must enter new password", username=username[0][0], grad_year=grad_year[0][0], curr_class=curr_class[0][0], concentration=concentration[0][0])

            # check if passwords match
            elif request.form.get("new_password") != request.form.get("new_password2"):
                return render_template("profile.html", error="passwords do not match", username=username[0][0], grad_year=grad_year[0][0], curr_class=curr_class[0][0], concentration=concentration[0][0])

            # search database for current password
            db.execute("SELECT hash FROM users WHERE id = (?)", (session["user_id"],))
            password = db.fetchall()

            # check if current password is correct
            if not check_password_hash(password[0][0], request.form.get("current_password")):
                return render_template("profile.html", error="invalid password", username=username[0][0], grad_year=grad_year[0][0], curr_class=curr_class[0][0], concentration=concentration[0][0])

            # update password (hash) in database
            db.execute("UPDATE users SET hash = (?) WHERE id = (?)", (generate_password_hash(request.form.get("new_password"), method='pbkdf2:sha256', salt_length=8), session["user_id"]))
            connection.commit()

            return render_template("profile.html", username=username[0][0], grad_year=grad_year[0][0], curr_class=curr_class[0][0], concentration=concentration[0][0])
            
        # check if user clicked button to change any of the other school-related information    
        elif request.form.get("action") == "school_info":
            # get graduation year of user
            db.execute("SELECT grad_year FROM users WHERE id = (?)", (session["user_id"],))
            grad_year = db.fetchall()
            
            # get class of user
            db.execute("SELECT class FROM users WHERE id = (?)", (session["user_id"],))
            curr_class = db.fetchall()
            
            # get concentration of user
            db.execute("SELECT concentration FROM users WHERE id = (?)", (session["user_id"],))
            concentration = db.fetchall()

            # if the user made a change to the graduation year, then update grad_year in database
            if request.form.get("years") != grad_year[0][0] and request.form.get("years") != "":
                db.execute("UPDATE users SET grad_year = (?) WHERE id = (?)", (request.form.get("years"), session["user_id"]))
                connection.commit()

            # if the user made a change to the class, then update class in database
            if request.form.get("classes") != curr_class[0][0] and request.form.get("classes") != "":
                db.execute("UPDATE users SET class = (?) WHERE id = (?)", (request.form.get("classes"), session["user_id"]))
                connection.commit()    

            # if the user made a change to the concentration, then update concentration in database
            if request.form.get("concentrations") != concentration[0][0] and request.form.get("concentrations") != "":
                db.execute("UPDATE users SET concentration = (?) WHERE id = (?)", (request.form.get("concentrations"), session["user_id"]))
                connection.commit()

        return redirect("/profile")
    
    else:
        return render_template("profile.html", username=username[0][0], grad_year=grad_year[0][0], curr_class=curr_class[0][0], concentration=concentration[0][0])

@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    # get all courses and corresponding scores (with join)
    db.execute("SELECT * FROM courses INNER JOIN scores ON scores.course_id = courses.id")
    courses = db.fetchall()

    if request.method == "POST":
        # if user didn't pick any criteria (blank option on dropdown), search by all criteria
        if request.form.get("criteria") == "":
            db.execute("SELECT * FROM courses INNER JOIN scores ON scores.course_id = courses.id WHERE (name LIKE '%' || (?) || '%' OR abbr LIKE '%' || (?) || '%' OR term LIKE '%' || (?) || '%' OR year LIKE '%' || (?) || '%' OR instructor LIKE '%' || (?) || '%' OR department LIKE '%' || (?) || '%' OR subject LIKE '%' || (?) || '%')", 
            (request.form.get("search"),request.form.get("search"),request.form.get("search"),request.form.get("search"),request.form.get("search"),request.form.get("search"),request.form.get("search")))
            courses = db.fetchall()

        # if user picked name criteria, search by course name
        elif request.form.get("criteria") == "name":
            db.execute("SELECT * FROM courses INNER JOIN scores ON scores.course_id = courses.id WHERE name LIKE '%' || ? || '%'", (request.form.get("search"),))
            courses = db.fetchall()

        # if user picked abbr criteria, search by course abbreviation
        elif request.form.get("criteria") == "abbr":
            db.execute("SELECT * FROM courses INNER JOIN scores ON scores.course_id = courses.id WHERE abbr LIKE '%' || ? || '%'", (request.form.get("search"),))
            courses = db.fetchall()

        # if user picked term criteria, search by course term
        elif request.form.get("criteria") == "term":
            db.execute("SELECT * FROM courses INNER JOIN scores ON scores.course_id = courses.id WHERE term LIKE '%' || ? || '%'", (request.form.get("search"),))
            courses = db.fetchall()

        # if user picked year criteria, search by course year
        elif request.form.get("criteria") == "year":
            db.execute("SELECT * FROM courses INNER JOIN scores ON scores.course_id = courses.id WHERE year LIKE '%' || ? || '%'", (request.form.get("search"),))
            courses = db.fetchall()

        # if user picked instructor criteria, search by course instructor
        elif request.form.get("criteria") == "instructor":
            db.execute("SELECT * FROM courses INNER JOIN scores ON scores.course_id = courses.id WHERE instructor LIKE '%' || ? || '%'", (request.form.get("search"),))
            courses = db.fetchall()

        # if user picked department criteria, search by course department
        elif request.form.get("criteria") == "department":
            db.execute("SELECT * FROM courses INNER JOIN scores ON scores.course_id = courses.id WHERE department LIKE '%' || ? || '%'", (request.form.get("search"),))
            courses = db.fetchall()

        # if user picked subject criteria, search by course subject
        elif request.form.get("criteria") == "subject":
            db.execute("SELECT * FROM courses INNER JOIN scores ON scores.course_id = courses.id WHERE subject LIKE '%' || ? || '%'", (request.form.get("search"),))
            courses = db.fetchall()

        return render_template("search.html", courses=courses)

    else:
        return render_template("search.html", courses=courses)

@app.route("/forum", methods=['GET', 'POST'])
@login_required
def forum():
    # get username, title, post, and timestamp from all posts
    db.execute("SELECT username, title, post, timestamp FROM posts ORDER BY timestamp DESC")
    posts = db.fetchall()

    if request.method == "POST":
        # check if title was entered
        if not request.form.get("title"):
            return render_template("forum.html", error="must enter title", posts=posts)

        # check if post content was entered
        elif not request.form.get("post"):
            return render_template("forum.html", error="must enter content", posts=posts)

        # get user's username
        db.execute("SELECT username FROM users WHERE id = (?)", (session["user_id"],))
        username = db.fetchall()

        # add new post
        db.execute("INSERT INTO posts (user_id, username, title, post) VALUES (?,?,?,?)",
        (session["user_id"], username[0][0], request.form.get("title"), request.form.get("post")))
        connection.commit()

        # retrieve post information ordered with newer posts first
        db.execute("SELECT username, title, post, timestamp FROM posts ORDER BY timestamp DESC")
        posts = db.fetchall()

        return render_template("forum.html", posts=posts)

    else:
        return render_template("forum.html", posts=posts)

