from sqlalchemy import null
from program import db, login_manager
from program import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)


    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Event(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    event_name = db.Column(db.String(length=50), nullable=False, unique=True)
    description = db.Column(db.String(length=1500), nullable=False, unique=True)
    date_start = db.Column(db.Date, nullable=False)
    date_end = db.Column(db.Date, nullable=False)
    google_link = db.Column(db.String(length=1024), nullable=False, unique=False)
    photo_link = db.Column(db.String(length=1024), nullable=False, unique=False)
    owner = db.Column(db.Integer(), nullable=False, unique=False)
    

class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    content = db.Column(db.String(length=240), nullable=False, unique=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    author_id = db.Column(db.Integer(), nullable=False, unique=False)
    event_id = db.Column(db.Integer(), nullable=False, unique=False)