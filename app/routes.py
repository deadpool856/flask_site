from flask import Blueprint, render_template, request
from flask import flash, redirect, url_for
from .models import Message
from . import db
from flask import session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from .models import User


main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        
        new_message = Message(name=name, message=message)
        db.session.add(new_message)
        db.session.commit()
        
        flash(f"Thank you, {name}. Your message has been saved!", "success")
        return redirect(url_for('main.contact'))
    
    return render_template('contact.html')

@main.route('/messages')
@login_required
def view_messages():
    messages = Message.query.all()
    return render_template('messages.html', messages=messages)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('main.view_messages'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.', 'info')
    return redirect(url_for('main.login'))
