from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from os import environ


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '6d84712a50d8a51fbde362773dd218eb'
app.config['FLASK_ADMIN_FLUID_LAYOUT'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'yeti'

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.id == 1:
            return True
        elif current_user.is_authenticated:
            return current_user.isAdmin
        else:
            return False

class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.id == 1:
            return True
        elif current_user.is_authenticated:
            return current_user.isAdmin
        else:
            return False

admin = Admin(app,template_mode='bootstrap4',index_view=MyAdminIndexView())

from program import routes
