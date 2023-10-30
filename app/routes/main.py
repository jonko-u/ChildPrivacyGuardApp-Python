from flask import Blueprint, render_template, request
from flask_login import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('main/index.html')

@main_bp.route('/about')
def about():
    return render_template('main/about.html')

@main_bp.route('/dashboard')
@login_required  # This route requires authentication
def dashboard():
    # Retrieve the username from the query parameter
    username = request.args.get('username')
    
    return render_template('main/dashboard.html', username=username)

@main_bp.route('/get_client_ip', methods=['GET'])
@login_required  # This route requires authentication
def get_client_ip():
    client_ip = request.remote_addr
    return f"{client_ip}"