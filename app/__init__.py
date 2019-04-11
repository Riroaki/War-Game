from flask import Flask
from flask_login import LoginManager
from app.config import Config
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, static_url_path='')
app.config.from_object(Config)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/itp'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
db = SQLAlchemy(app)

login_manager = LoginManager(app=app)
# login_manager.login_view = 'login'

from app import routes
