from flask import Blueprint, jsonify

status_blueprint = Blueprint('status', __name__)

@status_blueprint.route('/api/status')
def check_server_status():
    return jsonify({'server_status': 'online'})