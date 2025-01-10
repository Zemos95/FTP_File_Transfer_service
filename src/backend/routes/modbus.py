from flask import Blueprint, render_template, request, redirect, url_for, flash

modbus_blueprint = Blueprint('modbus', __name__)


@modbus_blueprint.route('/configuration', methods=['GET', 'POST'])
def configure():
    if request.method == 'POST':
        # Hier können Sie die Modbus-Konfiguration speichern
        flash('Modbus configuration saved successfully!', 'success')
        return redirect(url_for('modbus.configure'))
    return render_template('modbus.html')
