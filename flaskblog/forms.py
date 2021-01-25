from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TimeField
from wtforms.validators import DataRequired, InputRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class goingToSleepForm(FlaskForm):
    sleepStart = TimeField('When are you going to start your sleep?', validators=[InputRequired()])
    sleepEnd = TimeField('What is the time you have to be awake?', validators=[InputRequired()])
    submit = SubmitField('Get optimal wake up time')


class calibrateForm(FlaskForm):
    sleepStart = TimeField('What time did you go to sleep?', validators=[InputRequired()])
    sleepEnd = TimeField('What time did you wake up?', validators=[InputRequired()])
    submit = SubmitField('Get your faze!')


class howWasUrSleepForm(FlaskForm):
    sleepStart = TimeField('What time did you go to sleep?', validators=[InputRequired()])
    sleepEnd = TimeField('What time did you wake up?', validators=[InputRequired()])
    submit = SubmitField('Submit questionairy')
