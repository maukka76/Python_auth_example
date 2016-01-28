
from flask.ext.wtf import Form
from wtforms import SubmitField,StringField,PasswordField,HiddenField
from wtforms.validators import Required,Email

class LoginForm(Form):
	email = StringField('Enter your email',validators=[Required(),Email()])
	password = PasswordField('Enter your password',validators=[Required()])
	submit = SubmitField('Login');