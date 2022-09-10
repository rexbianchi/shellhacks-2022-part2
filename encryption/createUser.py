import os
import base64
# This is used to create a random 64 byte uuid
from secrets import randbits
# This is used to hash the password entered by the user to login
from hashlib import sha512
# These are used to encrypt and decrypt:
# - the uuid with the password hash
# - the .csv file with the uuid
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Get password from Rex in some form, probably from
# vault dictionary
uuid = ''
password = ''


# If there is no uuid i.e. a new user is being created,
# then make a random 512-bit uuid for that user
if not uuid:
    uuid = base64.urlsafe_b64encode(randbits(512))

salt = os.urandom(64)

# Key derivation function (encryptor)
kdf = PBKDF2HMAC(
    algorithm = hashes.SHA512(),
    length = 64,
    salt = salt,
    iterations = 480000
)

# Derives a hash from the provided password, then encodes
# it into a base64 key that will later be encrypted
key = base64.urlsafe_b64encode(kdf.derive(password))


f = Fernet(key)
token = f.encrypt(uuid)