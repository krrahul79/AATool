from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = '212241099d0eebcaa05efd779d93dd9660a79060080afd3e'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy(app)

from aatool import routes
