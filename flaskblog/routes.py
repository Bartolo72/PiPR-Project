from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, goingToSleepForm, calibrateForm, howWasUrSleepForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.calculator import calculateTime, calculatePhaze
from person import Person
from flaskblog.__init__ import database


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        username = current_user.username
        database.load_from_file()
        for user in database.people:
            if user.username == username:
                if user.sleptFlag == 1:
                    return redirect(url_for('how_was_your_sleep'))
                else:
                    break
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        person = Person(form.username.data)
        database.load_from_file()
        database.people.append(person)
        database.save_to_file(database.people)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')


@app.route('/going-to-sleep', methods=['GET', 'POST'])
def going_to_sleep():
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    if current_user.is_authenticated:
        username = current_user.username
        database.load_from_file()
        for user in database.people:
            if user.username == username:
                if user.sleptFlag == 1:
                    return redirect(url_for('how_was_your_sleep'))
                else:
                    break
    form = goingToSleepForm()
    if form.validate_on_submit():
        calculated = calculateTime(form.sleepStart.data, form.sleepEnd.data)
        flash(f"Your optimal wake up time is {calculated}", 'success')
    return render_template('going_to_sleep.html', title='Going to sleep', form=form)


@app.route('/calibrate', methods=['GET', 'POST'])
def calibrate():
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    form = calibrateForm()
    if form.validate_on_submit():
        calculated = calculatePhaze(form.sleepStart.data, form.sleepEnd.data)
        flash(f"Your sleep phaze lenght is {calculated} minutes. Your profile info has been updated", 'success')
    return render_template('calibrate.html', title='Calibrate', form=form)


@app.route("/how-was-your-sleep", methods=['GET', 'POST'])
def how_was_your_sleep():
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    form = howWasUrSleepForm()
    if form.validate_on_submit():
        cur_username = current_user.username
        database.load_from_file()
        for person in database.people:
            if person.username == cur_username:
                person.sleptFlag = 0
                for data in person.data:
                    if data.confirmed == False:
                        data.confirmed = True
                        break
                break
        database.save_to_file(database.people)
    return render_template('how_was_your_sleep.html', title='How was your sleep?', form=form)
