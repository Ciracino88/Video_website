from flask import Blueprint, redirect, url_for, render_template, request, session
from blueprints.catto import *
login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    recommended_username = generate_username_for_login()
    if request.method == 'POST':
        if request.form['login'] == 'login_by_custom':
            username = request.form['username']
            session['username'] = username

            return redirect(url_for('index.index'))

        if request.form['login'] == 'login_by_recommended':
            session['username'] = recommended_username
            print(recommended_username)

            return redirect(url_for('index.index'))

    return render_template('login.html')

@login_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index.index'))