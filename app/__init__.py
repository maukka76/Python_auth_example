from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'root'

db = SQLAlchemy(app)

#This decoration run once BEFORE any request
@app.before_first_request
def init_request():
	#This will create our db models
    db.create_all()

from app import routers