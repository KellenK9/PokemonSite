from flask import Flask
from flask import render_template
from flask import request
from flask import Flask, session
#from flask.ext.session import Session
import csv
import random
import hashlib

app = Flask(__name__)

app.secret_key = "super_secret_key123"

#SESSION_TYPE = 'redis'
#app.config.from_object(__name__)
#session(app)

@app.route("/")
def hello_world():
    return render_template("home.html")

@app.route("/home.html")
def display_home():
    return render_template("home.html")

@app.route("/login.html")
def display_login():
    return render_template("login.html")

@app.route("/register.html")
def display_register():
    return render_template("register.html")

@app.route("/course1.html")
def display_courses():
    return render_template("courses.html", class_name=class_name)

@app.route("/classes.html")
def display_classes():
    #We need a list of class names returned based on the logged in user
    if (session.get('username') != None):
        with open('database/users.csv', 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                if(session['username'] in row):
                    course_ids = row[5:]
        course_names = []
        with open('database/courses.csv', 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                for id in course_ids:
                    if(id == row[0]):
                        course_names.append(row[1])
        return render_template("classes.html", course_names=course_names)
    else:
        return render_template("classes.html")

@app.route("/user_page.html")
def display_user_page():
    return render_template("user_page.html")

@app.route("/new_user.html", methods=["post"])
def register_new_user():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    student_prof = request.form['student_prof']
    add_user(username, email, hash_password(password), student_prof)
    return render_template("home.html")

@app.route("/logout.html", methods=["post"])
def logout():
    session.pop('username', default=None)
    return render_template("home.html")

@app.route("/login_user.html", methods=["post"])
def login_user():
    username = request.form['username']
    password = request.form['password']
    valid_log_in = is_login_valid(username, hash_password(password))
    SESSION_TYPE = 'redis'
    app.config.from_object(__name__)
    #session(app)
    if valid_log_in:
        session['username'] = username
        return render_template("home.html")
    else:
        return render_template("login.html", error="invalid username or password")

@app.route("/course_search.html", methods=["post"])
def course_search():
    search = request.form['course_search']
    with open('database/courses.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        possible_courses = []
        for row in reader:
            if(search.lower() in row[1].lower() and row[1] != "course_name"):
                temp = [row[0], row[1]]
                possible_courses.append(temp)
    return render_template("user_page.html", possible_courses=possible_courses)

@app.route("/add_course.html", methods=["post"])
def add_course():
    course_id = request.form['course_to_add']
    with open('database/users.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        lines = []
        for row in reader:
            if(session['username'] in row):
                row.append(course_id)
                lines.append(row)
            else:
                lines.append(row)
    with open('database/users.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(lines)
    return render_template("/home.html")


def read_users_csv():
    with open('database/users.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')

def add_user(username, email, password, student_prof):
    with open('database/users.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        #Read last row and determine user_id or assign random userID
        user_id = random.randint(1000000, 9999999)
        writer.writerow([user_id, username, email, password, student_prof])

def is_login_valid(username, password):
    with open('database/users.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        valid = False
        for row in reader:
            if(username in row and password in row):
                valid = True
        return valid

def hash_password(password):
    h = hashlib.pbkdf2_hmac('sha256', b'password', b'salt', 100000)
    return h.hex()