from flask import Blueprint, render_template, request, current_app, flash
from flask_login import login_required, current_user
from flask_mail import Mail, Message
import datetime
from flask_recaptcha import ReCaptcha

from . import recaptcha
views = Blueprint('views', __name__)

messages = [['hello', 'test', '21:29'], [
    'hey there', 'test', '21:30'], ['yeah?', 'test', '21:31']]


# recaptcha = ReCaptcha(app=current_app)
# recaptcha = ReCaptcha()
# recaptcha.init_app(current_app)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        message = request.form.get('message')
        if message != messages[-1][0] and message != '':
            current_time = datetime.datetime.now()
            # current_time_formatted = current_time.strftime("%Y-%m-%d %H:%M:%S")
            current_time_formatted = current_time.strftime("%H:%M")
            messages.append(
                [message, current_user.nickname, current_time_formatted])
    return render_template('home.html', user=current_user, messages=messages)


@views.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        contact_message = request.form.get('contact-msg')
        if fullname == '' or email == '' or contact_message == '':
            flash('Please make sure you haven\'t left any empty fields.',
                  category='error')
        elif not recaptcha.verify():
            flash('Recaptcha error.', category='error')
        else:
            title = f'{email} {fullname}'
            msg = Message(title, sender='yagosik4@gmail.com',
                          recipients=['yagosik4@gmail.com'])
            msg.body = contact_message
            mail = Mail(current_app)
            mail.send(msg)
            flash('We appreciate you contacting DarkChat. One of our colleagues will get back in touch with you soon!', category='success')

    return render_template('contact.html', user=current_user)
