from flask.ext.login import UserMixin
#use: pip install flask-bcrypt
from flask.ext.bcrypt import generate_password_hash
from app import db

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String,unique=True)
	password = db.Column(db.String)
	friends = db.relationship('Friends',backref="user",primaryjoin='User.id==Friends.user_id',lazy='dynamic')
	
	
	def __init__(self, username, passw):
		self.username = username
		self.password = generate_password_hash(passw)



class Friends(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String)
	address = db.Column(db.String)
	age = db.Column(db.Integer)
	user_id= db.Column(db.Integer,db.ForeignKey('user.id'))
	
	def __init__(self, name, address,age,user_id):
		self.name = name
		self.address = address
		self.age = age
		self.user_id = user_id