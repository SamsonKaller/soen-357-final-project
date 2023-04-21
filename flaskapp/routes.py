import os
import secrets
import datetime
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskapp import app, db
from flaskapp.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskapp.models import User, Course, Assignment, Lecture
from flask_login import login_user, logout_user, login_required, current_user


def getCourseNames(courses):
    courseNames = []
    for course in courses:
        courseNames.append(course.name)
    return courseNames


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route("/")
@app.route("/home")
def home():
    courses = Course.query.all()
    return render_template('home.html', courses=courses)

    
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now sign in.', 'success')
        return redirect(url_for('login'))
    courseNames = getCourseNames(Course.query.all())
    return render_template('register.html', title='Register', courseNames=courseNames, form=form)

    
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and (user.password == form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    courseNames = getCourseNames(Course.query.all())
    return render_template('login.html', title='Login', courseNames=courseNames, form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
    

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    courseNames = getCourseNames(Course.query.all())
    return render_template('account.html', title='Account', courseNames=courseNames, image_file=image_file, form=form)


@app.route("/course/<string:coursename>", methods=['GET'])
def course(coursename):
    courseNames = getCourseNames(Course.query.all())
    course = Course.query.filter_by(name=coursename).first_or_404()
    filt = request.args.get('filt', '', type=str)
    
    return render_template('course.html', title=coursename, courseNames=courseNames, course=course, filt=filt)


@app.route("/chat")
def chat():
    courseNames = getCourseNames(Course.query.all())
    return render_template('chat.html', title='Chat', courseNames=courseNames)
    
    
@app.route("/calendar")
def calendar():
    courseNames = getCourseNames(Course.query.all())    
    return render_template('calendar.html', title='Calendar', courseNames=courseNames)
    

def populate_db():
    c1 = Course(name='COEN 316', teacher='Nicole Blue')
    c2 = Course(name='COEN 421', teacher='Jessica Simpson')
    c3 = Course(name='ELEC 372', teacher='Mathew Frank')
    c4 = Course(name='SOEN 357', teacher='Mister Goodday')
    db.session.add(c1)
    db.session.add(c2)
    db.session.add(c3)
    db.session.add(c4)
    
    
    db.session.add(Assignment(name='Assignment 1', week=1, date_due=datetime.datetime(2023, 1,  9), course=c1))
    db.session.add(Assignment(name='Assignment 2', week=2, date_due=datetime.datetime(2023, 1, 23), course=c1))
    db.session.add(Assignment(name='Assignment 3', week=3, date_due=datetime.datetime(2023, 2, 14), course=c1))
    db.session.add(Assignment(name='Assignment 4', week=4, date_due=datetime.datetime(2023, 2, 19), course=c1))
    db.session.add(Assignment(name='Assignment 5', week=5, date_due=datetime.datetime(2023, 3, 11), course=c1))
    db.session.add(Assignment(name='Assignment 6', week=6, date_due=datetime.datetime(2023, 3, 22), course=c1))

    
    db.session.add(Assignment(name='A1', week=1, date_due=datetime.datetime(2023, 1, 17), course=c2))
    db.session.add(Assignment(name='A2', week=2, date_due=datetime.datetime(2023, 1, 30), course=c2))
    db.session.add(Assignment(name='A3', week=3, date_due=datetime.datetime(2023, 2,  4), course=c2))
    db.session.add(Assignment(name='A4', week=4, date_due=datetime.datetime(2023, 2, 19), course=c2))
    db.session.add(Assignment(name='A5', week=5, date_due=datetime.datetime(2023, 3,  3), course=c2))
    db.session.add(Assignment(name='A6', week=6, date_due=datetime.datetime(2023, 3, 28), course=c2))

    
    db.session.add(Assignment(name= 'First Assignment', week=1, date_due=datetime.datetime(2023, 1, 19), course=c3))
    db.session.add(Assignment(name='Second Assignment', week=2, date_due=datetime.datetime(2023, 1, 29), course=c3))
    db.session.add(Assignment(name= 'Third Assignment', week=3, date_due=datetime.datetime(2023, 2, 13), course=c3))
    db.session.add(Assignment(name='Fourth Assignment', week=4, date_due=datetime.datetime(2023, 2, 28), course=c3))
    db.session.add(Assignment(name= 'Fifth Assignment', week=5, date_due=datetime.datetime(2023, 3,  8), course=c3))
    db.session.add(Assignment(name= 'Sixth Assignment', week=6, date_due=datetime.datetime(2023, 3, 25), course=c3))
    

    db.session.add(Assignment(name='Homework 1', week=1, date_due=datetime.datetime(2023, 1, 16), course=c4))
    db.session.add(Assignment(name='Homework 2', week=2, date_due=datetime.datetime(2023, 1, 30), course=c4))
    db.session.add(Assignment(name='Homework 3', week=3, date_due=datetime.datetime(2023, 2, 10), course=c4))
    db.session.add(Assignment(name='Homework 4', week=4, date_due=datetime.datetime(2023, 2, 22), course=c4))
    db.session.add(Assignment(name='Homework 5', week=5, date_due=datetime.datetime(2023, 3,  5), course=c4))
    db.session.add(Assignment(name='Homework 6', week=6, date_due=datetime.datetime(2023, 3, 14), course=c4))

    
    db.session.add(Lecture(name='Computer Technology', week=1, course=c1))
    db.session.add(Lecture(name='Performance',         week=2, course=c1))
    db.session.add(Lecture(name='Computer Language',   week=3, course=c1))
    db.session.add(Lecture(name='Pipelining',          week=4, course=c1))
    db.session.add(Lecture(name='Instructions',        week=5, course=c1))
    db.session.add(Lecture(name='the CPU',             week=6, course=c1))
    
    
    db.session.add(Lecture(name='Introduction',            week=1, course=c2))
    db.session.add(Lecture(name='Instruction Sets',        week=2, course=c2))
    db.session.add(Lecture(name='CPUs',                    week=3, course=c2))
    db.session.add(Lecture(name='Memory Mapping',          week=4, course=c2))
    db.session.add(Lecture(name='Interrupts',              week=5, course=c2))
    db.session.add(Lecture(name='Embedded Systems Design', week=6, course=c2))


    db.session.add(Lecture(name='Introduction',          week=1, course=c3))
    db.session.add(Lecture(name='Linearization',         week=2, course=c3))
    db.session.add(Lecture(name='Components of Systems', week=3, course=c3))
    db.session.add(Lecture(name='Nyquist Plots',         week=4, course=c3))
    db.session.add(Lecture(name='Transcombobulation',    week=5, course=c3))
    db.session.add(Lecture(name='Impossible Labs',       week=6, course=c3))


    db.session.add(Lecture(name='User Interaction Design', week=1, course=c4))
    db.session.add(Lecture(name='User Interface',          week=2, course=c4))
    db.session.add(Lecture(name='User Experience',         week=3, course=c4))
    db.session.add(Lecture(name='Cognition',               week=4, course=c4))
    db.session.add(Lecture(name='Mini-Project Info',       week=5, course=c4))
    db.session.add(Lecture(name='Final Project Info',      week=6, course=c4))


    db.session.commit()    
    return
    
@app.route('/fill_db')
def fill_db():
    populate_db()
    return redirect(url_for('home'))