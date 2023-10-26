from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
# from .models import User  # Import the User model
# from . import db  # Import the database instance
# from app import db
# from app.models import User
from app.forms import RegistrationForm
from app import db
from flask_login import UserMixin
from passlib.hash import sha256_crypt
from app.models import User

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
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # user = User.query.filter_by(username=username).first()

        # if user and user.check_password(password):
        #     login_user(user)
        #     flash('Login successful', 'success')
        #     return redirect(url_for('main.index'))
        # else:
        #     flash('Login failed. Please try again.', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    # logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('auth.login'))
