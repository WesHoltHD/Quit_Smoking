from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.models_user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#Main Route
@app.route("/")
def index():
    return render_template('/login.html')

#Register User - Post Method
@app.route('/register_user', methods=['POST'])
def register_user():
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'dob' : request.form['dob'],
        'email' : request.form['email'],
        'password' : request.form['password'],
        'confirm_password' : request.form['confirm_password']
    }
    valid = User.user_validator(data)
    if valid:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data['pw_hash'] = pw_hash
        user = User.create_user(data)
        session['user_id'] = user
        print('You got it, you are a new user')
        return redirect ('/inspire')
    return redirect ('/')

#Login User - Post Method
@app.route('/login_user', methods=['POST'])
def login_user():
    user = User.get_by_email(request.form)
    if not user:
        flash('Invalid Email', 'login')
        return redirect ('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid Password', 'login')
        return redirect ('/')
    session['user_id'] = user.id
    return redirect ('/dashboard')

#Logout User
@app.route ('/logout')
def logout():
    session.clear()
    return render_template('login.html')

