from base64 import b64encode
from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from app.picture_processing.picture_operations import blur_picture,encrypt_image, decrypt_image, download_image, upload_image, get_images,get_original_image_db
from app.picture_processing.totp_utils import generate_totp_password, verify_totp_password

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

        encoded_image= blur_picture(image, id_filename)
        return render_template('main/blur.html', encoded_image=encoded_image, id_filename=id_filename)
    
    # Handle the case where no image was uploaded
    return 'No image uploaded'

@main_bp.route('/display_pictures')  # You can define additional routes
@login_required  # This route requires authentication
def display_pictures():
    # Call a function to retrieve and display images
    images_metadata = get_images()  # You can create a function to fetch images                
        
    if images_metadata:
        # Render a template to display images
        return render_template('main/pictures.html', images=images_metadata)    
    else:
        # Handle the case where no images were found
        return 'No images available'


@main_bp.route('/get_original_picture', methods=['POST'])
@login_required
def get_original_picture():
    image_id = request.form.get('image_id')  # Get the image_id from the form data
    totp_password = generate_totp_password(secret=image_id)
    
    # Render the totp.html template, passing the image_id
    return render_template('main/totp.html', image_id=image_id, totp_password =totp_password)

@main_bp.route('/check_totp', methods=['POST'])
@login_required
def check_totp():
    image_id = request.form.get('image_id')
    totp_password = request.form.get('totp_password')
    
    # Verify the TOTP password
    check_totp_password = verify_totp_password(secret=image_id, user_input=totp_password)
    
    if check_totp_password:
        # If the TOTP is correct, retrieve the original image from the database
        encoded_image = get_original_image_db(image_id=image_id)
        
        # Render the 'original_picture.html' template with the image and TOTP details
        return render_template('main/original_picture.html', image_id=image_id, totp_password=totp_password, encoded_image=encoded_image)
    else:
        # If the TOTP is incorrect, redirect to the 'count_down.html' page
        return render_template('main/count_down.html')