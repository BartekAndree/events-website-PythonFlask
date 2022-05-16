from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from os import environ


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://zfzmrajlphftvt:aa52fb4c8b0a63fe933a914253d6c4c974648e212251ba5597df47d6f7f22e21@ec2-176-34-211-0.eu-west-1.compute.amazonaws.com:5432/de2uv1tee3jf28' # or 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '6d84712a50d8a51fbde362773dd218eb'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

from program import routes