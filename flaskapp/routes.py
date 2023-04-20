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
    courseNames = getCourseNames(Course.query.all())
    return render_template('home.html', courseNames=courseNames)

    
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


@app.route("/course/<string:coursename>")
def course(coursename):
    courseNames = getCourseNames(Course.query.all())
    course = Course.query.filter_by(name=coursename).first_or_404()    
    return render_template('course.html', title=coursename, courseNames=courseNames, course=course)


@app.route("/chat")
def chat():
    courseNames = getCourseNames(Course.query.all())
    return render_template('chat.html', title='Chat', courseNames=courseNames)
    
    
@app.route("/calendar")
def calendar():
    courseNames = getCourseNames(Course.query.all())    
    return render_template('calendar.html', title='Calendar', courseNames=courseNames)
    

def populate_db():
    c1 = Course(name='ELEC 372', teacher='Mathew Frank')
    c2 = Course(name='COEN 316', teacher='Nicole Blue')
    c3 = Course(name='COEN 421', teacher='Twit Twitley')
    c4 = Course(name='SOEN 357', teacher='Mister Goodday')
    db.session.add(c1)
    db.session.add(c2)
    db.session.add(c3)
    db.session.add(c4)
    
    a1 = Assignment(name='Assignment 1', date_due=datetime.datetime(2023, 4, 19), upload_file='elec372_ass1.pdf', course=c1)
    a2 = Assignment(name='Assignment 2', date_due=datetime.datetime(2023, 3, 3), upload_file='elec372_ass2.pdf', course=c1)
    a3 = Assignment(name='Assignment 3', date_due=datetime.datetime(2023, 2, 28), upload_file='elec372_ass3.pdf', course=c1)
    db.session.add(a1)
    db.session.add(a2)
    db.session.add(a3)
    
    a4 = Assignment(name='Assignment 1', date_due=datetime.datetime(2023, 1, 19), upload_file='coen316_ass1.pdf', course=c2)
    a5 = Assignment(name='Assignment 2', date_due=datetime.datetime(2023, 7, 3), upload_file='coen316_ass2.pdf', course=c2)
    a6 = Assignment(name='Assignment 3', date_due=datetime.datetime(2023, 5, 28), upload_file='coen316_ass3.pdf', course=c2)
    db.session.add(a4)
    db.session.add(a5)
    db.session.add(a6)
    
    a7 = Assignment(name='Assignment 1', date_due=datetime.datetime(2023, 1, 19), upload_file='coen421_ass1.pdf', course=c3)
    a8 = Assignment(name='Assignment 2', date_due=datetime.datetime(2023, 7, 3), upload_file='coen421_ass2.pdf', course=c3)
    a9 = Assignment(name='Assignment 3', date_due=datetime.datetime(2023, 5, 28), upload_file='coen421_ass3.pdf', course=c3)
    db.session.add(a7)
    db.session.add(a8)
    db.session.add(a9)    

    a10 = Assignment(name='Assignment 1', date_due=datetime.datetime(2023, 1, 19), upload_file='soen357_ass1.pdf', course=c4)
    a11 = Assignment(name='Assignment 2', date_due=datetime.datetime(2023, 7, 3), upload_file='soen357_ass2.pdf', course=c4)
    a12 = Assignment(name='Assignment 3', date_due=datetime.datetime(2023, 5, 28), upload_file='soen357_ass3.pdf', course=c4)
    db.session.add(a10)
    db.session.add(a11)
    db.session.add(a12)
    
    l1 = Lecture(name='Introduction', upload_file='elec372_lec1.pdf', course=c1)
    l2 = Lecture(name='Linearization', upload_file='elec372_lec2.pdf', course=c1)
    l3 = Lecture(name='Components of Systems', upload_file='elec372_lec3.pdf', course=c1)
    db.session.add(l1)
    db.session.add(l2)
    db.session.add(l3)
    
    l4 = Lecture(name='Computer Technology', upload_file='coen316_lec1.pdf', course=c2)
    l5 = Lecture(name='Performance', upload_file='coen316_lec2.pdf', course=c2)
    l6 = Lecture(name='Computer Language', upload_file='coen316_lec3.pdf', course=c2)
    db.session.add(l4)
    db.session.add(l5)
    db.session.add(l6)
    
    l7 = Lecture(name='Introduction', upload_file='coen421_lec1.pdf', course=c3)
    l8 = Lecture(name='Instruction Sets', upload_file='coen421_lec2.pdf', course=c3)
    l9 = Lecture(name='CPUs', upload_file='coen421_lec3.pdf', course=c3)
    db.session.add(l7)
    db.session.add(l8)
    db.session.add(l9)    

    l10 = Lecture(name='User Interaction Design', upload_file='soen357_lec1.pdf', course=c4)
    l11 = Lecture(name='User Interface', upload_file='soen357_lec2.pdf', course=c4)
    l12 = Lecture(name='User Experience', upload_file='soen357_lec3.pdf', course=c4)
    db.session.add(l10)
    db.session.add(l11)
    db.session.add(l12)

    db.session.commit()    
    return
    
@app.route('/fill_db')
def fill_db():
    populate_db()
    return redirect(url_for('home'))