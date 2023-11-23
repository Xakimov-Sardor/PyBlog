from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User, db
from flask_login import login_required, logout_user, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re



auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form.get
        email_or_username = data('email_or_username')
        password = data('password')

        user_login_with_email = User.query.filter_by(email=email_or_username).first()
        user_login_with_username = User.query.filter_by(username=email_or_username).first()


        if user_login_with_email:
            if check_password_hash(user_login_with_email.password, password):
                flash('Login successful', category='successful')

                login_user(user_login_with_email, remember=True)
                print('loggin with email ok')
                return redirect(url_for('views.home'))

            else:
                flash('Incorrect password', category='error')
        elif user_login_with_username:
            if check_password_hash(user_login_with_username.password, password):
                flash('Login successful', category='successful')

                login_user(user_login_with_username, remember=True)
                print('loggin with username ok')
                return redirect(url_for('views.home'))

            else:
                flash('Incorrect password', category='error')
        elif not user_login_with_email or not user_login_with_username:
            flash('There is no registered user with this name or email, you can signup')
        else:
            flash('Sorry, something error please try again', category='error')
            print('sorry')

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required 
def logout():
    logout_user()


    return redirect(url_for('views.home'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.form.get

        username = data('username')
        email = data('email')
        password = data('password')
        repassword = data('repassword')

        # TEMPLATE_FOR_USERNAME = '^[a-z0-9_-]{3,15}$'
        # TEMPLATE_FOR_PASSWORD = '^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$'
        TEMPLATE_FOR_EMAIL = '[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+'

        user_email_exist = User.query.filter_by(email=email).first()
        user_name_exist = User.query.filter_by(username=username).first()
        

        if user_name_exist:
            flash('This username has already been registered', category='error')
            print('name error')
        elif not re.match(TEMPLATE_FOR_EMAIL, email):
            flash('Enter the correct format for email', category='error')
            print('emil error 1')
        elif user_email_exist:
            flash('This email has already been registered', category='error')
            print('email error 2')
        elif not len(password) > 8:
            flash('The password is not secure enough', category='error')
            print('password error 1')
        elif password != repassword:
            flash('Passwords did not match')
            print('password error 2')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password, method='scrypt')) # createing new user model and hashing(for security) password
            db.session.add(new_user) # add new user to database
            db.session.commit() # save changes to database

            login_user(new_user, remember=True)

            flash('New user created!', category='successful')
            print('new user created')

            return redirect(url_for('views.home'))

    return render_template('signup.html', user=current_user)
