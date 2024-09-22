from flask import Blueprint, redirect, url_for, render_template, request, session

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username

        return redirect(url_for('index.index'))

    return render_template('login.html')

@login_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index.index'))