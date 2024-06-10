import base64
import jwt, requests
from config import Config

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

import logging
logger = logging.getLogger(__name__)

_cachedKey = None
_cachedUrl = None

# Create a session that doesn't verify SSL certificates
session = requests.Session()
session.verify = False # TODO figure out how to add a certificate

def split_key_into_chunks(key, chunk_size=64):
    return [key[i:i+chunk_size] for i in range(0, len(key), chunk_size)]

def getPublicKey():
    global _cachedKey, _cachedUrl

    if not _cachedUrl:
        url = f'{Config.AUTH_DOMAIN}/.well-known/openid-configuration'
        response = session.get(url)
        _cachedUrl = response.json()['jwks_uri']

    if not _cachedKey:
        response = session.get(_cachedUrl)
        _cachedKey = response.json()['keys'][0]['x5c'][0]
    
    # Decode the base64-encoded certificate and load it
    cert_der = base64.b64decode(_cachedKey)
    cert = x509.load_der_x509_certificate(cert_der, default_backend())

    # Extract the public key from the certificate
    public_key = cert.public_key()

    # Serialize the public key to PEM format
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return pem.decode('utf-8')

def testToken(token):
    key = getPublicKey()
    try:
        data = jwt.decode(
            token, 
            key, 
            verify=True, 
            algorithms=['RS256'],
            audience='account'
        )
        return data
    except jwt.PyJWTError as e:
        print(e)
        return None

def getUserType(token):
    key = getPublicKey()
    data = jwt.decode(
        token, 
        key, 
        verify=True, 
        algorithms=['RS256'],
        audience='account'
    )

    return data['realm_access']['roles']

def isManager(token):
    try:
        roles = getUserType(token)
        return "manager" in roles
    except jwt.PyJWTError as e:
        print(e)
        return False


def isAgent(token):
    try:
        roles = getUserType(token)
        return 'agent' in roles
    except jwt.PyJWTError:
        return False
    
def getUserName(token):
    try:
        data = testToken(token)
        return data['preferred_username']
    except jwt.PyJWTError as e:
        print(e)
        return None