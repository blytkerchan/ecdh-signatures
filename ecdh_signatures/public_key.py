'''Public keys for use in verification'''
import base64
import sys
from cryptography.hazmat.primitives import serialization

class PublicKey:
    '''Public keys for use in verification'''
    def __init__(self, public_key):
        self._public_key = public_key

    def save(self, output):
        encoded = self._public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        b64_encoded = base64.b64encode(encoded)
        output.write(f'pubkey={str(b64_encoded, encoding="utf-8")}\n')

    @classmethod
    def load(cls, inp):
        '''Load a public key from file'''
        encoded = None
        for line in inp.readlines():
            s = line.split('=', 1)
            if s[0] == 'pubkey':
                b64_encoded = s[1]
                encoded = base64.b64decode(b64_encoded)
            else:
                print(f'Unknown line type {s[0]}, ignoring', file=sys.stderr)
        if not encoded:
            raise ValueError('No public key found in input')
        public_key = serialization.load_der_public_key(encoded)
        return PublicKey(public_key)
