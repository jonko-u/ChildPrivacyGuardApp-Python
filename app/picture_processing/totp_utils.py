from base64 import b32encode
import pyotp


def generate_totp_secret():
    """
    Generate a new TOTP secret key and return it.
    Store this secret securely in your database.
    """
    new_secret = pyotp.random_base32()
    return new_secret

def generate_totp_uri(secret, label, issuer, digits=6, period=30):
    """
    Generate a TOTP URI based on the secret, label, issuer, and other parameters.
    This URI can be used to generate QR codes for TOTP setup.
    """
    totp = pyotp.TOTP(secret, interval=period)
    uri = totp.provisioning_uri(name=label, issuer_name=issuer)
    return uri

def generate_totp_password(secret):
    """
    Generate a TOTP password based on the provided secret.
    """
    # Convert the string to bytes
    secret_bytes = secret.encode('utf-8')

    # Encode the bytes to Base32
    secret_base32 = b32encode(secret_bytes).decode('utf-8')
    totp = pyotp.TOTP(secret_base32)
    password = totp.now()
    return password

def verify_totp_password(secret, user_input):
    """
    Verify a user's TOTP password against the provided secret.
    Return True if the password is valid, False otherwise.
    """
    # Convert the string to bytes
    secret_bytes = secret.encode('utf-8')

    # Encode the bytes to Base32
    secret_base32 = b32encode(secret_bytes).decode('utf-8')
    totp = pyotp.TOTP(secret_base32)
    return totp.verify(user_input)

def save_totp_password_to_file(image_id):
    # Generate the totp password
    password = generate_totp_password(image_id)
    # Save the TOTP password to a text file
    with open('totp.txt', 'w') as totp_file:
        totp_file.write(password)