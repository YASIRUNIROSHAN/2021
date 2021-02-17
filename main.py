from flask import Flask, render_template, Response, request, redirect, url_for
import cv2
from flask_sqlalchemy import SQLAlchemy

from authentication import get_frame
from registration import get_fr

app = Flask(__name__)
app.debug = True

DATA = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='root',
                                                                             password='mypass',
                                                                             server='localhost',
                                                                             database='flaskapp1')

app.config['SQLALCHEMY_DATABASE_URI'] = DATA
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    regNum = db.Column(db.String(100))
    department = db.Column(db.String(100))
    email = db.Column(db.String(100))
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, fname,lname, regNum,department, email,username, password):
        self.fname = fname
        self.lname = lname
        self.regNum = regNum
        self.department = department
        self.email = email
        self.username = username
        self.password = password


face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('model/trained_model2.yml')


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/fetch_data', methods=['POST', 'GET'])
def FetchData():
    if request.method == "POST":
        user = request.form['username']
        password = request.form['password']
        details = Student.query.filter_by(username=user).all()
        if details == []:
            error = "Username doesn't exists."
            return render_template("login.html", error=error)
            # return "<h1>Username doesn't exists.</h1>"
        else:
            for detail in details:
                uname = detail.username
                regNu = detail.regNum
                passw = detail.password
            if uname == user:
                if password == passw:
                    return redirect(url_for('Authentication', regNum=regNu))
                else:
                    error = "Invalid Username or password."
                    # return redirect(request.url)
                    return render_template("login.html", error=error)

            else:
                error = "Username doesn't exists."
                return render_template("login.html", error=error)
            # return redirect(url_for('Success', name=user, passwrd=password))
    else:
        user = request.form['username']
        password = request.form['password']
        details = Student.query.filter_by(username=user).all()
        if details == []:
            error = "Username doesn't exists."
            return render_template("login.html", error=error)
            # return "<h1>Username doesn't exists.</h1>"
        else:
            for detail in details:
                uname = detail.username
                regNu = detail.regNum
                passw = detail.password
            if uname == user:
                if password == passw:
                    return redirect(url_for('Authentication', regNum=regNu))
                else:
                    error = "Invalid Username or password"
                    return render_template("login.html", error=error)
            else:
                error = "Username doesn't exists."
                return render_template("login.html", error=error)


@app.route('/video_feed')
def video_feed():
    return render_template("signup.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/redirect')
def Redirect():
    return render_template("home.html")

@app.route('/authentication/<regNum>')
def Authentication(regNum):
    id = regNum
    print(id)
    count, invalid = get_frame(id)
    print(count)
    if count == 20 or invalid < 50:
        return render_template('coursepage.html')
    else:
        error = "User didn't match with the Register Number"
        return redirect(url_for('Redirect',error=error))


@app.route('/registerWebcam/<fname>/<regNum>')
def RegisterWebcam(fname, regNum):
    name = fname
    id = regNum
    fr = get_fr(name, id)
    ff=10
    print(fr)
    if ff == 10:
        return redirect(url_for('Redirect'))
    else:
        return render_template('signup.html')


# @app.route('/registered/<name>/<passwrd>/<cnfpass>')
# def Registered(name, passwrd, cnfpass):
#     if passwrd == cnfpass:
#         print(name,passwrd)
#
#         database.update({name: passwrd})
#         return redirect(url_for('RegisterWebcam'))
#     else:
#         return render_template("signup.html", message="Password didn't matched.")
#

@app.route('/signup', methods=['POST', 'GET'])
def Signup():
    if request.method == "POST":
        StudentDetails = request.form
        firstname = request.form['firstname']
        print(firstname)
        lastname = StudentDetails['lastname']
        regNum = StudentDetails['regNum']
        department = StudentDetails['department']
        email = StudentDetails['email']
        username = StudentDetails['username']
        password = StudentDetails['password']
        conPassword = StudentDetails['conPassword']

        if password == conPassword:
            my_data = Student(firstname,lastname, regNum,department, email,username, password)
            db.session.add(my_data)
            db.session.commit()
            return redirect(url_for('RegisterWebcam', fname=firstname, regNum=regNum))
        else:
            error = "Password and Confirm Password didn't matched"
            return render_template("signup.html", error=error)

    else:
        StudentDetails = request.form
        firstname = StudentDetails['firstname']
        lastname = StudentDetails['lastname']
        regNum = StudentDetails['regNum']
        department = StudentDetails['department']
        email = StudentDetails['email']
        username = StudentDetails['username']
        password = StudentDetails['password']
        conPassword = StudentDetails['conPassword']

        if password == conPassword:
            my_data = Student(firstname, lastname, regNum, department, email, username, password)
            db.session.add(my_data)
            db.session.commit()
            return redirect(url_for('RegisterWebcam'))
        else:
            error = "Password and Confirm Password didn't matched"
            return render_template("signup.html", error=error)

# @app.route('/exam')
# def headPose():
#     hp=headPose()
#     # return render_template("signup.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
