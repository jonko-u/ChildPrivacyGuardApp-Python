from pymongo import MongoClient
from gridfs import GridFS
from PIL import Image
import io
from bson import ObjectId
from cryptography.fernet import Fernet

from dotenv import load_dotenv
import os
import logging

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
    image_binary = io.BytesIO()
    image.save(image_binary, format='JPEG')  # You can change the format as needed

    encrypted_image_data = encrypt_image(image_binary=image_binary, encryption_key=secret_key)

    id_filename = ObjectId()

    # Create a GridFS object and store the image
    fs = GridFS(db)
    fs.put(encrypted_image_data, filename=image_filename, _id= id_filename)

    return id_filename

def encrypt_image(image_binary, encryption_key):    
    fernet = Fernet(encryption_key)
    encrypted_image_data = fernet.encrypt(image_binary.getvalue())
    return encrypted_image_data

def decrypt_image():

    # Connecto to mongodb
    db = connect_to_mongodb()

    # Create a Fernet object with the key
    fernet = Fernet(secret_key)

    image_id = ObjectId("654060104cfccebbf67bdcb1")  # Replace with the correct ObjectID

    # Query the image by ID
    # Create a GridFS object
    fs = GridFS(db, collection="fs")
    encrypted_data = fs.find_one(filter={"_id" : image_id})
    logging.warning(encrypted_data)
    
    # Decrypt the data
    decrypted_data = fernet.decrypt(encrypted_data.read())

    image = Image.open(io.BytesIO(decrypted_data))
    logging.warning(image)
    # Specify the output filename and extension
    output_filename = 'outputfile.jpg'  # Change the filename and extension as needed

    # Save the image to the local file
    image.save(output_filename)

    print(f"Image saved locally as {output_filename}")

def download_image():

    # Connecto to mongodb
    db = connect_to_mongodb()

    image_id = ObjectId("654022bd927bb66bc693ed59")  # Replace with the correct ObjectID

    # Query the image by ID
    # Create a GridFS object
    fs = GridFS(db, collection="fs")
    encrypted_data = fs.find_one(filter={"_id" : image_id})
    # Decrypt the data
    print(encrypted_data)
    image = Image.open(io.BytesIO(encrypted_data.read()))

    # Specify the output filename and extension
    output_filename = 'outputfile.jpg'  # Change the filename and extension as needed

    # Save the image to the local file
    image.save(output_filename)

    print(f"Image saved locally as {output_filename}")