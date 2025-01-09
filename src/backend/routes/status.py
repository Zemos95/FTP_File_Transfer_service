from flask import Blueprint, jsonify

status_blueprint = Blueprint('status', __name__)


@status_blueprint.route('/api/status', methods=['GET'])
def get_status():
    # Hier können Sie den tatsächlichen Serverstatus abrufen
    server_status = 'online'  # oder 'offline'
    return jsonify({'server_status': server_status})


@status_blueprint.route('/api/login_status', methods=['GET'])
def get_login_status():
    # Hier können Sie den tatsächlichen Login-Status abrufen
    login_status = 'success'  # oder 'failed'
    return jsonify({'login_status': login_status})
