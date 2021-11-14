from flask import Flask, request, g
from flask import render_template
from flask import Flask, session
import csv
import os
import sys
import random

app = Flask(__name__)

app.config.from_object(__name__)

app.secret_key = "super_secret_key123"

with open('pokemon.csv', encoding="utf-16") as f:
    csv_reader = csv.reader(f, delimiter='\t')
    reader = list(csv_reader)

@app.route('/comparison.html')
def search():
    global poke_names
    return render_template('textboxes.html')

@app.route('/comparison.html', methods=['POST'])
def comparison():
    poke1 = str(request.form['text1']).lower()
    poke2 = str(request.form['text2']).lower()

    for i in range(len(reader)):
        if str(reader[i][2]).lower() == poke1:
            num1 = i
        if str(reader[i][2]).lower() == poke2:
            num2 = i

    attack1 = reader[num1][14]
    defense1 = reader[num1][15]
    hp1 = reader[num1][13]
    spattack1 = reader[num1][16]
    spdefense1 = reader[num1][17]
    speed1 = reader[num1][18]
    type11 = reader[num1][4]
    type12 = reader[num1][5]
    total1 = int(hp1) + int(attack1) + int(defense1) + int(spattack1) + int(spdefense1) + int(speed1)

    attack2 = reader[num2][14]
    defense2 = reader[num2][15]
    hp2 = reader[num2][13]
    spattack2 = reader[num2][16]
    spdefense2 = reader[num2][17]
    speed2 = reader[num2][18]
    type21 = reader[num2][4]
    type22 = reader[num2][5]
    total2 = int(hp2) + int(attack2) + int(defense2) + int(spattack2) + int(spdefense2) + int(speed2)

    return render_template('display.html', pokemon1 = poke1, pokemon2 = poke2, attack1 = attack1, attack2 = attack2, total1 = total1, total2 = total2, defense1 = defense1, defense2 = defense2, hp1 = hp1, hp2 = hp2, spattack1 = spattack1, spattack2 = spattack2, spdefense1 = spdefense1, spdefense2 = spdefense2, speed1 = speed1, speed2 = speed2, type11 = type11, type12 = type12, type21 = type21, type22 = type22)

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
    add_user(username, email, password, student_prof) #hash password
    return render_template("home.html")

@app.route("/logout.html", methods=["post"])
def logout():
    session.pop('username', default=None)
    return render_template("home.html")

@app.route("/login_user.html", methods=["post"])
def login_user():
    username = request.form['username']
    password = request.form['password']
    valid_log_in = is_login_valid(username, password) #Hash passwords
    SESSION_TYPE = 'redis'
    app.config.from_object(__name__)
    #session(app)
    if valid_log_in:
        session['username'] = username
        return render_template("home.html")
    else:
        return render_template("login.html", error="invalid username or password")

#Functions (Not Flask Routes): 

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

#def hash_password(password):
    #h = hashlib.pbkdf2_hmac('sha256', b'password', b'salt', 100000)
    #return h.hex()







#Keep this at end of code
if __name__ == '__main__':
    port = os.environ.get("PORT", 5000)
    app.run(debug=False, host="0.0.0.0", port=port)
