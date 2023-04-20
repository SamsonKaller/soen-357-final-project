import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskapp import app, db
from flaskapp.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskapp.models import User
from flask_login import login_user, logout_user, login_required, current_user


courses = ['ELEC 372', 'COEN 316', 'COEN 421', 'SOEN 357']


courseContent = {
    'ELEC 372' : {
        'lectures' : ['week1.pdf', 'week2.pdf', 'week3.pdf', 'week4.pdf', 'week5.pdf'],
        'assignments' : ['hw1.pdf', 'hw2.pdf', 'hw3.pdf', 'hw4.pdf', 'hw5.pdf'],
        'grades' : {
            'hw1.pdf' : 20.0,
            'hw2.pdf' : 55.5,
            'hw3.pdf' : 85.75,
            'hw4.pdf' : 44.0,
            'hw5.pdf' : 69.0
        }
    },
    'COEN 316' : {
        'lectures' : ['week1.pdf', 'week2.pdf', 'week3.pdf', 'week4.pdf', 'week5.pdf'],
        'assignments' : ['hw1.pdf', 'hw2.pdf', 'hw3.pdf', 'hw4.pdf', 'hw5.pdf'],
        'grades' : {
            'hw1.pdf' : 20.0,
            'hw2.pdf' : 55.5,
            'hw3.pdf' : 85.75,
            'hw4.pdf' : 44.0,
            'hw5.pdf' : 69.0
        }
    },
    'COEN 421' : {
        'lectures' : ['week1.pdf', 'week2.pdf', 'week3.pdf', 'week4.pdf', 'week5.pdf'],
        'assignments' : ['hw1.pdf', 'hw2.pdf', 'hw3.pdf', 'hw4.pdf', 'hw5.pdf'],
        'grades' : {
            'hw1.pdf' : 20.0,
            'hw2.pdf' : 55.5,
            'hw3.pdf' : 85.75,
            'hw4.pdf' : 44.0,
            'hw5.pdf' : 69.0
        }
    },
    'SOEN 357' : {
        'lectures' : ['week1.pdf', 'week2.pdf', 'week3.pdf', 'week4.pdf', 'week5.pdf'],
        'assignments' : ['hw1.pdf', 'hw2.pdf', 'hw3.pdf', 'hw4.pdf', 'hw5.pdf'],
        'grades' : {
            'hw1.pdf' : 20.0,
            'hw2.pdf' : 55.5,
            'hw3.pdf' : 85.75,
            'hw4.pdf' : 44.0,
            'hw5.pdf' : 69.0
        }
    }
}


@app.route("/")
@app.route("/home")
def home():
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
    return render_template('register.html', title='Register', courses=courses, form=form)

    
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
    return render_template('login.html', title='Login', courses=courses, form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
    

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
    return render_template('account.html', title='Account', courses=courses, image_file=image_file, form=form)


@app.route("/course/<string:coursename>")
def course(coursename):
    return render_template('course.html', title=coursename, courses=courses, courseContent=courseContent[coursename])


@app.route("/chat")
def chat():
    return render_template('chat.html', title='Chat', courses=courses)
    
@app.route("/calendar")
def calendar():
    return render_template('calendar.html', title='Calendar', courses=courses)