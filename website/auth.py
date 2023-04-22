# the views related to authentication reside here

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
# below import imports the dependencies for the password hashing task
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
# these functions below work with the caches of the browser
# and the server to remember a user session. 
# remembering the user session helps the user to remain
# logged in unless he logs out manually
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('User does not exist.', category='error')

    return render_template("login.html", user=current_user)

# the decorator '@login_required' makes sure that we are not able
# to access this page unless we are logged in

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) <4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(first_name) <2:
            flash('First name must be atleast 2 characters long.', category='error')
        elif password1 != password2:
            flash('Passwords dont match!', category='error')
        elif len(password1) <7:
            flash('Password must be atleast 7 characters long.', category='error')
        else:
            #add to database
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

    '''
    users stored during testing:
    pinto@p.com
    r@s.com
    rajat@singh.com
    pass: 12345678
    '''