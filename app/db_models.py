from flask.ext.login import UserMixin
from app import db
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String)
	password = db.Column(db.String)
	def __init__(self, username, password):
		self.username = username
		self.password = password

class Friends(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String)
	address = db.Column(db.String)
	age = db.Column(db.Integer)
	user_id= db.Column(db.Integer,db.ForeignKey('user.id'))
