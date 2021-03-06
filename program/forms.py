from enum import unique
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField, URLField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from program.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Login')

class AddEventForm(FlaskForm):
    event_name = StringField(label='Event Name:', validators=[Length(min=6, max=50), DataRequired()])
    description = TextAreaField(label='Description:', validators=[Length(max=1500), DataRequired()])
    date_start = DateField(label='Date Start:', validators=[DataRequired()])
    date_end = DateField(label='Date End:', validators=[DataRequired()])
    google_link = URLField(label='Google Link:', validators=[DataRequired()])
    photo_link = URLField(label='Photo Link:', validators=[DataRequired()])
    submit = SubmitField(label='Add Event')

class AddCommentForm(FlaskForm):
    comment = TextAreaField(label='Comment:', validators=[Length(max=240), DataRequired()])
    submit = SubmitField(label='Add Comment')

class SetFullName(FlaskForm):
    full_name = StringField(label='Full Name:', validators=[Length(min=4, max=30), DataRequired()])
    submit = SubmitField(label='Save changes kurwa')
