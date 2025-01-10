from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from ..models.user import User, users

login_blueprint = Blueprint('login', __name__)


@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = users.get(username)
        if user and user.check_password(password):
            login_user(user)
            flash('Login erfolgreich!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('home.home'))
        flash('Ungültiger Benutzername oder Passwort.', 'danger')
  
    return render_template('login.html')


@login_blueprint.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Erfolgreich ausgeloggt!', 'info')
    return redirect(url_for('login.login'))