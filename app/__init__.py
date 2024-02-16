from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///craft_project_manager.db'
app.config['SECRET_KEY'] = '3617'

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

migrate = Migrate(app, db)

from app.models import User
from app import routes

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
