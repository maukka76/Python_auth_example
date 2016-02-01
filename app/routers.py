from app import app
from flask import render_template,request,abort,flash,redirect,url_for
from app.forms import LoginForm,FriendForm,UpdateForm
from app.db_models import User,Friends
from app import db
from flask.ext.bcrypt import check_password_hash
from app import login_manager
from flask.ext.login import login_user,login_required,logout_user,current_user

@app.route('/',methods=['GET','POST'])
def root():
	login_form = LoginForm()
	if request.method == 'GET':
		return render_template('index.html',form=login_form)
	if login_form.validate_on_submit():
		user = User.query.filter_by(username=login_form.email.data)
		if user.count() == 1 and check_password_hash(user[0].password,login_form.password.data):
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
	#You can use also our backref to get the friends for this user....
	print(user.friends.all())
	friends = User.query.join(Friends,user.id==Friends.user_id).add_columns(User.id,Friends.id,Friends.name,Friends.address,Friends.age).filter(User.id==user.id).all()
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

@app.route('/delete/<int:id>')
def deleteFriend(id):
	friend = Friends.query.get(id)
	db.session.delete(friend)
	db.session.commit()
	flash('Friend deleted succcessfully.')
	return redirect('/data')

@app.route('/update/<int:id>')
def updateFriendView(id):
	friend = Friends.query.get(id)
	form = UpdateForm();
	form.hidden.data = friend.id
	form.name.data = friend.name
	form.address.data = friend.address
	form.age.data = friend.age
	return render_template('update.html',form=form)

@app.route('/update',methods=['POST'])
def updateFriend():
	form = UpdateForm();
	friend = Friends.query.get(form.hidden.data)
	if form.validate_on_submit():
		form.hidden.data = friend.id
		friend.name = form.name.data
		friend.address = form.address.data
		friend.age = form.age.data
		db.session.commit()
		return redirect('/data')
	else:
		flash('Fill up all the asked infromation!')
		return render_template('update.html',form=form)
	
@login_manager.user_loader
def user_loader(user_id):
    user = User.query.filter_by(id=user_id)
    if user.count() == 1:
        return user.one()
    return None