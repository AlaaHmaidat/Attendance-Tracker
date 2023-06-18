from flask import Flask,send_file
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask import render_template, url_for, flash, redirect
# from forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from flask_login import UserMixin
from tokenize import String
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, Email, ValidationError
import glob
# ################
from flask import Flask, render_template, request
import cv2
import os
import numpy as np
import pandas as pd
from datetime import date, datetime
import time
from sklearn.neighbors import KNeighborsClassifier
import joblib
app = Flask(__name__)
app.config["SECRET_KEY"] = "62913a7dac3933f87a84626fcdeaaf9e2653f0a000843efd9bf2b31ba4767402"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrybt = Bcrypt(app)
login_manager = LoginManager(app)

def datetoday():
    return date.today().strftime("%m_%d_%y")

def datetoday2():
    return date.today().strftime("%d-%B-%Y")


if not os.path.isdir('Attendance'):
    os.makedirs('Attendance')
if not os.path.isdir('static/faces'):
    os.makedirs('static/faces')
if f'Attendance-{datetoday()}.csv' not in os.listdir('Attendance'):
    with open(f'Attendance/Attendance-{datetoday()}.csv', 'w') as f:
        f.write('Name,ID,Time,Date')
        


def load_model():
    if 'face_recognition_model.pkl' in os.listdir('static'):
        return joblib.load('static/face_recognition_model.pkl')
    return None

def totalreg():
    return len(os.listdir('static/faces'))

def extract_faces(img):
    face_detector = cv2.CascadeClassifier('static/haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_points = face_detector.detectMultiScale(gray, 1.3, 5)
    return face_points

def identify_face(facearray, model):
    if model is not None:
        return model.predict(facearray)
    return []

def train_model():
    faces = []
    labels = []
    userlist = os.listdir('static/faces')
    for user in userlist:
        for imgname in os.listdir(f'static/faces/{user}'):
            img = cv2.imread(f'static/faces/{user}/{imgname}')
            resized_face = cv2.resize(img, (50, 50))
            faces.append(resized_face.ravel())
            labels.append(user)
    faces = np.array(faces)
    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(faces, labels)
    joblib.dump(model, 'static/face_recognition_model.pkl')

# def extract_attendance():
#     df=""
#     df = pd.read_csv(f'Attendance/Attendance-{datetoday()}.csv')
#     if current_user.is_authenticated and current_user.role=='student':
#         df = pd.read_csv(f'Attendance/Attendance-{current_user.username}.csv')
#     names = df['Name']
#     IDs = df['ID']
#     times = df['Time']
#     l = len(df)
#     return names, IDs, times, l
def extract_attendance():
    if current_user.is_authenticated:

        if not os.path.exists(f'Attendance/Attendance-{current_user.username}.csv'):
            with open(f'Attendance/Attendance-{current_user.username}.csv', "w") as file:
                file.write('Name,ID,Time,Date')
    df=""
    df = pd.read_csv(f'Attendance/Attendance-{datetoday()}.csv')
    if current_user.is_authenticated and current_user.role=='student':
        
        df = pd.read_csv(f'Attendance/Attendance-{current_user.username}.csv')
    names = df['Name']
    IDs = df['ID']
    times = df['Time']
    dates = df['Date']
    l = len(df)
    return names, IDs, times,dates, l

def face_verified():
    df=""
    # df = pd.read_csv(f'static/faces/{current_user.username}_{str(current_user.id)}/{current_user.username}_{str(current_user.id)}.jpg')
    if not os.path.isdir(f'static/faces/{current_user.username}_{str(current_user.id)}'):
        return False
    else:
        return True
    

    
# def extract_attendance():
    
#     folder_path = 'Attendance'
#     file_list = os.listdir(folder_path)
#     file_list.sort(key=lambda x: os.path.getmtime(os.path.join(folder_path, x)))
    
#     last_file = os.path.join(folder_path, file_list[-2])
    
#     if  current_user.is_authenticated and current_user.role=='student':
#         last_file = os.path.join(folder_path, file_list[-1])
#     df = pd.read_csv(last_file)
#     names = df['Name']
#     rolls = df['ID']
#     times = df['Time']
#     l = len(df)

#     return names, rolls, times, l 

# def extaract_specific_student():
#     folder_path = 'Attendance'
#     file_list = os.listdir(folder_path)
#     file_list.sort(key=lambda x: os.path.getmtime(os.path.join(folder_path, x)))
#     last_file = os.path.join(folder_path, file_list[-1])

#     if current_user.id==df['ID']:

#         df = pd.read_csv(last_file)
#         names = df['Name']
#         rolls = df['ID']
#         times = df['Time']
#         l = len(df)

#     return names, rolls, times, l 

# def extract_user_attendance():
#     user_id = current_user.id
#     username = current_user.username
#     csv_files = glob.glob(f'Attendance/Attendance-{username}*.csv')
#     all_attendance = []

#     for file in csv_files:
#         df = pd.read_csv(file)
#         user_attendance = df[df['ID'] == user_id]
#         all_attendance.append(user_attendance)

#     if len(all_attendance) > 0:
#         merged_df = pd.concat(all_attendance)
#         return merged_df['Name'], merged_df['ID'], merged_df['Time'], len(merged_df)

#     return[],[],[],0

def add_attendance(name):
    
    if f'Attendance-{current_user.username}.csv' not in os.listdir('Attendance'):
        with open(f'Attendance/Attendance-{current_user.username}.csv', 'w') as f:
            f.write('Name,ID,Time')
    username = name.split('_')[0]
    userid = name.split('_')[1]
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = date.today()

    df = pd.read_csv(f'Attendance/Attendance-{datetoday()}.csv')
    if int(userid) not in list(df['ID']):
        with open(f'Attendance/Attendance-{datetoday()}.csv', 'a') as f:
            f.write(f'\n{username},{userid},{current_time},{current_date}')
    
    df = pd.read_csv(f'Attendance/Attendance-{current_user.username}.csv')
    if int(userid) not in list(df['ID']):
        with open(f'Attendance/Attendance-{current_user.username}.csv', 'a') as f:
            f.write(f'\n{username},{userid},{current_time},{current_date}')

def home():
    if current_user.is_authenticated and current_user.role=='student':
        names, rolls, times,dates, l = extract_attendance()
        return render_template('home.html', names=names, rolls=rolls, times=times, l=l, totalreg=totalreg(), datetoday2=datetoday2(),dates=dates)
    else:
        return render_template('home.html')

def Features():
    names, rolls, times,dates, l = extract_attendance()
    return render_template('Features.html', names=names, rolls=rolls, times=times, l=l, totalreg=totalreg(), datetoday2=datetoday2(),dates=dates)

def start():
    model = load_model()
    if model is None:
        return render_template('home.html', totalreg=totalreg(), datetoday2=datetoday2(),
                               mess='There is no trained model in the static folder. Please add a new face to continue.')

    cap = cv2.VideoCapture(0)
    ret = True
    start_time = time.time()
    while ret:
        ret, frame = cap.read()
        if extract_faces(frame) != ():
            (x, y, w, h) = extract_faces(frame)[0]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 20), 2)
            face = cv2.resize(frame[y:y+h, x:x+w], (50, 50))
            identified_person = identify_face(face.reshape(1, -1), model)[0]
            add_attendance(identified_person)
            cv2.putText(frame, f'{identified_person}', (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 20), 2, cv2.LINE_AA)

        elapsed_time = time.time() - start_time
        if elapsed_time >= 7:
            break

        cv2.imshow('Attendance', frame)
        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()
    names, rolls, times,dates, l = extract_attendance()
    return render_template('Attendance.html', names=names, rolls=rolls, times=times, l=l, totalreg=totalreg(), datetoday2=datetoday2(),dates=dates)

def add():
    cap = cv2.VideoCapture(0)
    newusername = current_user.username
    # newusername = "ahmad"
    newuserid =current_user.id
    # newuserid = 12345
    userimagefolder = 'static/faces/' + newusername + '_' + str(newuserid)
    if not os.path.isdir(userimagefolder):
        os.makedirs(userimagefolder)

    i, j = 0, 0
    while 1:
        _, frame = cap.read()
        faces = extract_faces(frame)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 20), 2)
            cv2.putText(frame, f'Images Captured: {i}/50', (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 20), 2, cv2.LINE_AA)
            if j % 10 == 0:
                name = newusername + '_' + str(i) + '.jpg'
                cv2.imwrite(userimagefolder + '/' + name, frame[y:y+h, x:x+w])
                i += 1
            j += 1
        if j == 500:
            break
        cv2.imshow('Adding new User', frame)
        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()
    train_model()
    names, rolls, times,dates, l = extract_attendance()
    var=face_verified()
    # return redirect('Attendance.html', names=names, rolls=rolls, times=times, l=l, totalreg=totalreg(), datetoday2=datetoday2(), var=var)
    return redirect(url_for("Attendance"))

def download_attendance():
        attendance_file = f'Attendance/Attendance-{datetoday()}.csv'
        return send_file(attendance_file, as_attachment=True)


def run():
   
    
    
    app.add_url_rule('/', 'home', home)
    app.add_url_rule('/home', 'home', home)
    # app.add_url_rule('/demo', 'demo', demo)
    app.add_url_rule('/Attendance', 'Attendance', attendance)
    app.add_url_rule('/Price', 'Price', price)
    app.add_url_rule('/Contact', 'Contact', contact)
    app.add_url_rule('/about', 'about', about)
    app.add_url_rule('/start', 'start', start, methods=['GET'])
    app.add_url_rule('/Features', 'Features', Features)
    app.add_url_rule('/add', 'add', add, methods=['GET', 'POST'])
    app.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])
    app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
    app.add_url_rule('/logout', 'logout', logout)
    app.add_url_rule('/download_attendance', 'download_attendance', download_attendance)

    app.run(debug=True)




#####################


def attendance():
    """Render the home page."""
    names, rolls, times,dates, l = extract_attendance()
    
   
    if current_user.is_authenticated:
        ver=face_verified()
        return render_template('Attendance.html', names=names, rolls=rolls, times=times, l=l, totalreg=totalreg(), datetoday2=datetoday2(),ver=ver,dates=dates)
            
            
        
    else:
        flash("You have to login first", "warning")
        return redirect(url_for("login"))

def price():
    """Render the home page."""
    return render_template("Price.html", title="Price")
def contact():
    """Render the home page."""
    return render_template("Contact.html", title="Contact")

# def demo():
#     """Render the home page."""
#     if not current_user.is_authenticated:
#         return redirect(url_for("login"))
#     return render_template("demo.html", title="demo")
    


# def home():
#     """Render the home page."""
#     return render_template("home.html", title="Home")


@app.route("/about")
def about():
    """Render the about page."""
    return render_template("about.html", title="About")


def register():
    """Handle user registration."""
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrybt.generate_password_hash(form.password.data).decode('utf-8')
        # if form.role.data == "student":
        student = Student(
            fname=form.fname.data,
            lname=form.lname.data,
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            role=form.role.data,

        )
        db.session.add(student)
        db.session.commit()
        # elif form.role.data == "instructor":
        #     instructor = Instructor(
        #         fname=form.fname.data,
        #         lname=form.lname.data,
        #         username=form.username.data,
        #         email=form.email.data,
        #         password=hashed_password,
        #     )
            # db.session.add(instructor)
            # db.session.commit()
        flash(f"Account created successfully for {form.username.data}", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


# @app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(email=form.email.data).first()
        # instructor = Instructor.query.filter_by(email=form.email.data).first()
        if student and bcrybt.check_password_hash(student.password, form.password.data):
            flash("Login Successful", "success")
            login_user(student, remember=form.remember.data)
            return redirect(url_for("home"))
        # elif instructor and bcrybt.check_password_hash(instructor.password, form.password.data):
        #     flash("Login Successful", "success")
        #     login_user(instructor, remember=form.remember.data)
        #     return redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("login.html", title="Login", form=form)




# @app.route("/logout")
def logout():
    """Handle user logout."""
    logout_user()
    flash(f"Logged out successfully ", "success")
    return redirect(url_for("home"))

class RegistrationForm(FlaskForm):
    """Form for user registration."""
    fname = StringField("First Name", validators=[DataRequired(), Length(min=2, max=25)])
    lname = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=25)])
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    role = RadioField('Role', choices=[('student', 'Student'), ('instructor', 'Instructor')], validators=[DataRequired()], default='student')
    password = PasswordField("Password", validators=[DataRequired(), Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_])[A-Za-z\d@$!%*?&_]{8,32}$")])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        """Validate the uniqueness of the username."""
        student = Student.query.filter_by(username=username.data).first()
        # instructor = Instructor.query.filter_by(username=username.data).first()
        # if student or instructor:
        if student:

            raise ValidationError("Username already exists! Please choose a different one")

    def validate_email(self, email):
        """Validate the uniqueness of the email address."""
        student = Student.query.filter_by(username=email.data).first()
        # instructor = Instructor.query.filter_by(username=username.data).first()
        # if student or instructor:
        if student:

            raise ValidationError("Email already exists! Please choose a different one")



class LoginForm(FlaskForm):
    """Form for user login."""
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

# database
@login_manager.user_loader
def load_user(user_id):
    """Load the user object from the user ID stored in the session."""
    return Student.query.get(int(user_id))

class Student(db.Model, UserMixin):
    """Class representing a student."""
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='student')

    def __repr__(self):
        """Return a string representation of the Student object."""
        return f"Student('{self.fname}', '{self.lname}', '{self.username}', '{self.email}')"


# class Instructor(db.Model, UserMixin):
#     """Class representing an instructor."""
#     id = db.Column(db.Integer, primary_key=True, nullable=False)
#     fname = db.Column(db.String(25), nullable=False)
#     lname = db.Column(db.String(25), nullable=False)
#     username = db.Column(db.String(25), nullable=False, unique=True)
#     email = db.Column(db.String(120), nullable=False, unique=True)
#     password = db.Column(db.String(100), nullable=False)
#     role = db.Column(db.String(10), nullable=False, default='instructor')


    def __repr__(self):
        """Return a string representation of the Instructor object."""
        return f"Instructor('{self.fname}', '{self.lname}', '{self.username}', '{self.email}')"


class Course(db.Model):
    """Class representing a course."""
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(25), nullable=False)
    description = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        """Return a string representation of the Course object."""
        return f"Course('{self.name}', '{self.description}')"


class Lesson(db.Model):
    """Class representing a lesson."""
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(25), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

    def __repr__(self):
        """Return a string representation of the Lesson object."""
        return f"Lesson('{self.title}', '{self.course_id}')"


class Attendance(db.Model):
    """Class representing student attendance for each lesson."""
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    presence_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_present = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        """Return a string representation of the Attendance object."""
        return f"Attendance('{self.student_id}', '{self.lesson_id}', '{self.is_present}')"




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    run()
