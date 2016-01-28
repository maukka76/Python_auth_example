
from flask.ext.wtf import Form
from wtforms import SubmitField,StringField,PasswordField,IntegerField
from wtforms.validators import Required,Email,NumberRange

class LoginForm(Form):
	email = StringField('Enter your email',validators=[Required(),Email()])
	password = PasswordField('Enter your password',validators=[Required()])
	submit = SubmitField('Login');
	
class FriendForm(Form):
	name = StringField('Enter your name',validators=[Required()])
	address = StringField('Enter your address',validators=[Required()])
	age = IntegerField('Enter you age',validators=[NumberRange(0,120)])
	submit = SubmitField('Send');