from flask import Blueprint, render_template, request
from flask_login import login_required
from app.picture_processing.picture_operations import encrypt_image, decrypt_image, download_image, upload_image

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

@main_bp.route('/picture_process', methods=['POST'])
@login_required  # This route requires authentication
def picture_process():
    if 'image' in request.files:
        image = request.files['image']
        # Process the uploaded image here (e.g., save it to a folder, apply operations)
        image_filename = image.filename
        # Example: Save the image to a folder on the server
        id_filename = upload_image(image=image, image_filename=image_filename)



        return f'Image uploaded and processed successfully {id_filename} '
    
    # Handle the case where no image was uploaded
    return 'No image uploaded'

@main_bp.route('/picture_decrypted')
@login_required  # This route requires authentication
def picture_decrypted():
    
    decrypt_image()
    # Handle the case where no image was uploaded
    return 'Image is there'