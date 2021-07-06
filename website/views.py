from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
import datetime
from flask_mail import Mail, Message
views = Blueprint('views', __name__)

messages = [['hello', 'test', '21:29'], [
    'hey there', 'test', '21:30'], ['yeah?', 'test', '21:31']]


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
        contact_message = request.form.get('contact-msg')

    return render_template('contact.html', user=current_user)
