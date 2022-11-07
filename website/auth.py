from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
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
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

#default logout function to return signup page
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

#sign up page
@auth.route('/sign-up', methods=['GET', 'POST'])
#autorization function
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        #troubleshooting any problem
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Please, choose another email', category='error')
        elif len(email) < 5:
            flash('Please, write more than 4 characters.', category='error')
        elif len(first_name) < 5:
            flash('Please, write more than 4 characters.', category='error')
        elif password1 != password2:
            flash('Passwords are not same, try again', category='error')
        elif len(password1) < 8:
            flash('Please, write more than 7 characters.', category='error')
        else:
            #creating new database for new user
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User succesfully created!', category='success')
            #directing to main page
            return redirect(url_for('views.home'))




    
    return render_template("sign_up.html", user=current_user)
