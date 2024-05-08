import re

from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from . import db
from .models import User

users = []
auth = Blueprint("auth", __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        #     flash('Invalid email format', 'error')

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')  # Hash the password
        # print(generate_password_hash(password, method='pbkdf2:sha256'))
        # Create a new user
        new_user = User(username=username, email=email, password=hashed_password)
        # print(len(hashed_password))
        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        return redirect(url_for('auth.login'))
    else:
        return render_template('signup.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        # two = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        # one = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        # print('1 st time:', one)
        # print('2 ed time:', two)
        # print('result:::', check_password_hash(one, two))
        if user:
            if check_password_hash(user.password, request.form['password']):
                login_user(user, remember=True)
                return redirect(url_for('task_manager.index'))
            else:
                return render_template('login.html', error='Wrong Password')
        else:
            return render_template('login.html', error='Invalid email')
    else:
        return render_template('login.html')


@auth.route('/change_pass', methods=['GET', 'POST'])
def change_pass():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        prev_pass = request.form['password']
        new_pass = request.form['new_password']
        if user and check_password_hash(user.password, prev_pass):
            # print('prev pass:', prev_pass)
            # print('new pass:', new_pass)
            user.password = generate_password_hash(new_pass, method='pbkdf2:sha256')
            db.session.commit()
            return redirect(url_for('auth.login'))
        elif not user:
            return render_template('change_pass.html', error='Invalid email')
        else:
            return render_template('change_pass.html', error='Wrong Password')
    else:
        return render_template('change_pass.html')
            

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    # session.pop('user_id', None)  # Clear user ID from session
    return redirect(url_for('auth.login'))