from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Successfuly!', category='success')
                login_user(user)
                return redirect(url_for('views.home'))
            else:
                flash('The password is incorrect.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout Successfuly!', category='success')
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        nickname = request.form.get('nickname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        i_agree = request.form.get('i-agree')
        print(i_agree)

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')

        elif len(nickname) < 2:
            flash('Nickname must be greater than 2 characters.', category='error')
        elif password1 != password2:
            flash('Passwords must match.', category='error')
        elif len(password1) < 5:
            flash('Password should contain at least 5 characters.', category='error')
        elif i_agree != 'accept':
            flash('You must accept terms and conditions!', category='error')
        else:
            new_user = User(email=email, nickname=nickname, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash('Account Created!', category='success')
            title = 'Ready to get started!?'
            msg = Message(title, sender='yagosik4@gmail.com',
                          recipients=[email])
            message_body = f'Dear {nickname}, \r\n Welcome to the DarkChat! \r\n I’m very excited to have you as a part of the DarkChat community! \r\n If you have any questions, concerns or just want to say ’hi’ you can reach out to me any time. \r\n Cheers, \r\n Yaron'
            msg.body = message_body
            mail = Mail(current_app)
            mail.send(msg)
            return redirect(url_for('views.home'))

    return render_template('signup.html', user=current_user)
