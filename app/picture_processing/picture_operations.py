from pymongo import MongoClient
from gridfs import GridFS
from PIL import Image
from io import BytesIO
from bson import ObjectId
from cryptography.fernet import Fernet
import face_recognition
from dotenv import load_dotenv
import os
import cv2
import numpy as np
from base64 import b32encode, b64encode

# Load environment variables from .env
load_dotenv()

secret_key = os.getenv("SECRET_FILE_KEY")

def connect_to_mongodb():
    
    # Access the environment variables
    mongodb_url = os.getenv("MONGODB_LOCAL_URL")
    mongodb = os.getenv("MONGODB_LOCAL_DB")
    client = MongoClient(mongodb_url)
    db = client[mongodb]  # Replace 'securezone001' with your database name
    return db

# Function to encrypt and upload an image
def upload_image(image, image_filename):
    # Connect to MongoDB
    db = connect_to_mongodb()

    # Load the image using Pillow (PIL)
    image = Image.open(image)
    # Convert the image to binary data
    image_binary = BytesIO()
    image.save(image_binary, format='JPEG')  # You can change the format as needed

    encrypted_image_data = encrypt_image(image_binary=image_binary, encryption_key=secret_key)

    id_filename = ObjectId()

    # Create a GridFS object and store the image
    fs = GridFS(db, "fese")
    fs.put(encrypted_image_data, filename=image_filename, _id= id_filename)

    return id_filename

def encrypt_image(image_binary, encryption_key):    
    # Create a Fernet object with the key
    fernet = Fernet(encryption_key)
    # Encrypt the data of the image
    encrypted_image_data = fernet.encrypt(image_binary.getvalue())
    return encrypted_image_data

def decrypt_image(image_id, db):

    # Create a Fernet object with the key
    fernet = Fernet(secret_key)    
    # Create a GridFS object
    fs = GridFS(db, collection="fese")
    encrypted_data = fs.find_one(filter={"_id" : image_id})    
    # Decrypt the data
    decrypted_data = fernet.decrypt(encrypted_data.read())
    return decrypted_data
    
def download_image(image_data):

    image = Image.open(BytesIO(image_data))

    # Specify the output filename and extension
    output_filename = 'outputfile.jpg'  # Change the filename and extension as needed

    # Save the image to the local file
    image.save(output_filename)

    print(f"Image saved locally as {output_filename}")

def blur_picture(image, id_filename):    
    # Connecto to mongodb
    db = connect_to_mongodb()

    coordenates_of_boxes = {                                             
                        }
    # Load image
    image_recog = face_recognition.load_image_file(image)
    # Find face locations in the image
    face_locations = face_recognition.face_locations(image_recog)

    # Convert the image to OpenCV format
    image_cv2 = cv2.cvtColor(image_recog, cv2.COLOR_RGB2BGR)

    # Define the blurring kernel size (you can adjust this)
    blur_kernel = (99, 99)
    
    # Initialize a counter for the box IDs
    box_id = 1
    # Blur all detected faces
    for face_location in face_locations:
        top, right, bottom, left = face_location
        face = image_cv2[top:bottom, left:right]
        face = cv2.GaussianBlur(face, blur_kernel, 30)
        image_cv2[top:bottom, left:right] = face
        # Collect coordinates for the current box and add it to the dictionary
        coordenates_of_boxes[str(box_id)] = {
            'top': str(top),
            'right': str(right),
            'bottom': str(bottom),
            'left': str(left)
        }
        # Increment the box ID
        box_id += 1
    # Convert the OpenCV image back to RGB format
    processed_image = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB)
    
    id_filename_blured = ObjectId()
    # Save the processed image to a byte buffer
    output_buffer = BytesIO()
    Image.fromarray(processed_image).save(output_buffer, format="JPEG")
    output_buffer.seek(0)
    fs = GridFS(db, "blur")
    fs.put(output_buffer.getvalue(), filename=image.filename, _id= id_filename_blured, original_picture_id=id_filename, coordenates_of_boxes = coordenates_of_boxes)
    
    # Serialize the data to a JSON string

    encoded_image = b64encode(output_buffer.read()).decode('utf-8')
    
    return encoded_image


# Function to retrieve and decrypt images
def get_images():
    db = connect_to_mongodb()
    # Create a GridFS object
    fs = GridFS(db,collection="blur")

    # Retrieve the image metadata from the 'my_custom_files' collection
    image_metadata = fs.find({})
    # Create a dict where  { id : encoded_image}
    images_loaded_dict = {}
    # Loop al the images_metadata are
    for file_info in image_metadata: 
        # Read the file info       
        image_data = file_info.read()
        # Encode the image metadata in base64
        encoded_image = b64encode(image_data).decode('utf-8')
        # Save in our dict the {id : encoded_image}
        images_loaded_dict[str(file_info._id)] = encoded_image
        
    return images_loaded_dict


def get_original_image_db(image_id):
    # Connect to mongo database
    db = connect_to_mongodb()
    # Create a GridFS object
    fs = GridFS(db,collection="blur")
    # Find the id of our blurred image
    image_metadata = fs.find_one({"_id": ObjectId(image_id)})
    # Get the id of the original picture
    original_picture_id = image_metadata.original_picture_id
    # Decrypt the image data
    decrypted_data = decrypt_image(image_id=original_picture_id, db=db)
    # Encode in base64 our clean data
    encoded_image = b64encode(decrypted_data).decode('utf-8')

    return encoded_image
    

