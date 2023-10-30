from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename
import os

component_bp = Blueprint('component', __name__, url_prefix='/component')

# Define a directory to store uploaded files
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Function to check if a file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@component_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            flash('File uploaded successfully', 'success')
            return redirect(url_for('component.upload_file'))
        else:
            flash('Invalid file format', 'danger')
            return redirect(request.url)
    return render_template('component/upload.html')


# Other component-related routes and functions can be defined here

