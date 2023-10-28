from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, login_required, logout_user# from .models import User  # Import the User model
# from . import db  # Import the database instance
# from app import db
# from app.models import User
from app.forms import LoginForm, RegistrationForm
from app.database import db
from passlib.hash import sha256_crypt
from app.models import User
from app.models import UserLogin
import logging

auth_bp = Blueprint('auth', __name__)



@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        password = form.password.data
        hashed_password = sha256_crypt.hash(password)
        user = User(username=form.username.data, email=form.email.data, password = hashed_password )        
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. You can now log in.', 'success')
        user.is_active = True
        login_user(user)
        return redirect(url_for('main.dashboard'))
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()  # Create an instance of the form

    if form.validate_on_submit():  # Check if the form was submitted and is valid
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        
        is_pass_valid = sha256_crypt.verify(password, user.password)
        logging.warning(is_pass_valid)
        if user and is_pass_valid:     
            user.is_active = True       
            login_user(user)
            return redirect(url_for('main.dashboard', username=username))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    # logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('auth.login'))
