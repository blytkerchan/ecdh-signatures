'''KeyPair class'''
import base64
import os
import sys
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from .public_key import PublicKey

class KeyPair:
    '''KeyPair class.

    Implements the basic operations for a key pair, including loading, saving, and generation (as a class method)'''
    def __init__(self, private_key, public_key):
        self._private_key = private_key
        self._public_key = public_key

    def public_key(self):
        '''Get the public key'''
        return PublicKey(self._public_key)

    def save(self, keyfile, password):
        '''Save the key to a file, encrypted with a password, and using a random salt that is also saved'''
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
            )
        key = kdf.derive(password.encode('utf-8'))
        serialized_private = self._private_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(key)
            )
        b64_serialized_private = base64.b64encode(serialized_private)
        b64_salt = base64.b64encode(salt)
        with open(keyfile, 'x', encoding='utf-8') as f:
            f.writelines(
                [f'salt={str(b64_salt, encoding="utf-8")}\n',
                f'key={str(b64_serialized_private, encoding="utf-8")}\n'
                ])

    @classmethod
    def generate(cls, curve):
        '''Generate a new keypair'''
        private_key = ec.generate_private_key(curve)
        public_key = private_key.public_key()
        return KeyPair(private_key, public_key)

    @classmethod
    def load(cls, keyfile, password):
        '''Load a keypair from a file using a given password'''
        salt = None
        serialized_private = None
        with open(keyfile, 'r', encoding='utf-8') as k:
            for line in k.readlines():
                s = line.split('=', 1)
                if s[0] == 'salt':
                    salt = base64.b64decode(s[1])
                elif s[0] == 'key':
                    serialized_private = base64.b64decode(s[1])
                else:
                    print(f'Unknown line type {s[0]}, ignoring', file=sys.stderr)
        if not salt or not serialized_private:
            raise ValueError('Missing information in keyfile, aborting', file=sys.stderr)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
            )
        key = kdf.derive(password.encode('utf-8'))
        private_key = serialization.load_der_private_key(
            data=serialized_private,
            password=key,
            )
        public_key = private_key.public_key()
        key_pair = KeyPair(private_key, public_key)
        return key_pair

