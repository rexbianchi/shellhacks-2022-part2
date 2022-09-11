import os
import base64
import json

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

def readJSON(fileName):
    with open('./vaults.json') as file:
        vaults = json.load(file)["vaults"]
    return vaults

def hashForNewPass(password):
    salt = os.urandom(64)
    kdf = PBKDF2HMAC(
        algorithm = hashes.SHA512(),
        length = 64,
        salt = salt,
        iterations = 480000
    )

    dKey = base64.urlsafe_b64encode(kdf.derive(password))
    return {
        "key": dKey,
        "salt": salt
    }

def hashForExistingPass(vaultSalt, password):
    # Key derivation function (encryptor)
    kdf = PBKDF2HMAC(
        algorithm = hashes.SHA512(),
        length = 64,
        salt = vaultSalt,
        iterations = 480000
    )

    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

def decrypt(encryptedText, vaultName, password):
    vaults = readJSON('./vaults.json')
    vaultInfo = vaults[vaultName]
    
    # Derivation Key
    dKey = hashForExistingPass(vaultInfo.get('salt'), password)

    f = Fernet(dKey)
    uuid = f.decrypt(vaultInfo.get('eKey'))
    
    g = Fernet(uuid)
    plainText = g.decrypt(encryptedText)
    
    return plainText

def new_account(fileLoc, vaultName, password):
    vaults = readJSON('./vaults.json')
    keyAndSalt = hashForNewPass(password)

    # Generates a uuid for a new user
    uuid = Fernet.generate_key()
    f = Fernet(keyAndSalt['key'])
    
    eKey = f.encrypt(uuid)

    newVaultInfo = {
        "fileLoc": fileLoc,
        "eKey": eKey,
        "salt": keyAndSalt['salt']
    }

    vaults[vaultName] = newVaultInfo
    with open('./vaults.json', 'w') as file:
        json.dump({"vaults": vaults}, file)
    
    
def encrypt(plainText, vaultName, password):
    vaults = readJSON('./vaults.json')
    vaultInfo = vaults[vaultName]

    dKey = hashForExistingPass(vaultInfo.get('salt'), password)

    f = Fernet(dKey)
    uuid = f.decrypt(vaults.get('eKey'))

    g = Fernet(uuid)
    encryptedText = g.encrypt(plainText)
    
    return encryptedText