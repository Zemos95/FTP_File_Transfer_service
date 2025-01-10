from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from ..models.user import User

login_blueprint = Blueprint('login', __name__)

# Dummy-Benutzer (ersetzen Sie dies durch eine echte Benutzerverwaltung)
users = {
    'admin': User(id=1, username='admin', password='password')  # Passwort sollte gehasht werden
}

@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = users.get(username)
        if user and user.password == password:
            login_user(user)
            flash('Erfolgreich eingeloggt!', 'success')
            return redirect(url_for('home.home'))
        else:
            flash('Ungültige Anmeldedaten.', 'danger')

    return render_template('login.html')

@login_blueprint.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Erfolgreich ausgeloggt!', 'info')
    return redirect(url_for('login.login'))