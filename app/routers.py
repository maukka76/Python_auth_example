from app import app
from flask import render_template,request,abort,flash,redirect,url_for
from app.forms import LoginForm,FriendForm
from app.db_models import User,Friends
from app import db
from app import login_manager
from flask.ext.login import login_user,login_required,logout_user,current_user

@app.route('/',methods=['GET','POST'])
def root():
	login_form = LoginForm()
	if request.method == 'GET':
		return render_template('index.html',form=login_form)
	if login_form.validate_on_submit():
		user = User.query.filter_by(username=login_form.email.data).filter_by(password=login_form.password.data)
		if user.count() == 1:
			login_user(user.one())
			return redirect('/data')
		else:
			flash('Invalid username or password')
			return redirect('/')
	else:
		flash('Give proper email address')
		return redirect('/')
		
@app.route('/register', methods=['GET', 'POST'])
def register():
	message = None
	form = LoginForm()
	if request.method == 'GET':
		return render_template('register.html',form=form)
	elif request.method == 'POST':
		if form.validate_on_submit():
			user = User.query.filter_by(username=form.email.data)
			if user.count() == 0:
				user = User(form.email.data,form.password.data)
				db.session.add(user)
				db.session.commit()
				flash('Username {0} registered'.format(form.email.data))
				return redirect('/')
			else:
				flash('Username {0} allready in use. Try some other'.format(form.email.data))
				return redirect('/register')
		else:
			return render_template('register.html',form=form,message='Invalid email address!')
				
	else:
		abort(405)

@app.route('/data')
@login_required
def secret():
	user = User.query.get(current_user.id)
	friends = User.query.join(Friends,user.id==Friends.user_id).add_columns(User.id,Friends.name,Friends.address,Friends.age).filter(User.id==user.id).all()
	print(len(friends))
	temp = len(friends)
	return render_template('secret_data.html',fr=friends,length=temp)

@app.route('/friends',methods=['GET','POST'])
@login_required
def addFriend():
	fForm = FriendForm()
	if request.method == 'GET':
		return render_template('friends.html',form=fForm)
	else:
		if fForm.validate_on_submit():
			temp = Friends(fForm.name.data,fForm.address.data,fForm.age.data,current_user.id)
			db.session.add(temp)
			db.session.commit()
			return redirect('/data')
		else:
			flash('Give correct information to fields!')
			return render_template('friends.html',form=fForm)
		

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@login_manager.user_loader
def user_loader(user_id):
    user = User.query.filter_by(id=user_id)
    if user.count() == 1:
        return user.one()
    return None