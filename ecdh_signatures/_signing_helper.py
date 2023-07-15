'''Helper class for signing'''
import base64
import sys
from ._constants import HASH_ALGORITHMS as _HASH_ALGORITHMS
from .key_pair import KeyPair
from argparse import Namespace
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.hmac import HMAC

class SigningHelper:
    '''Helper class for signing. Implements the protocol'''
    def __init__(self, curve):
        self._curve = curve

    def generate_keypair(self):
        '''Generate a keypair'''
        return KeyPair.generate(self._curve)

    def keypair_from_hash(self, h):
        '''Generate a keypair from a hash. One wouldn't normally do this, but it's part of the protocol'''
        private_key = ec.derive_private_key(int.from_bytes(h, byteorder='big'), self._curve)
        public_key = private_key.public_key()
        return KeyPair(private_key, public_key)

    @classmethod
    def hash(cls, algorithm, data):
        '''Hash a value with a given algorithm'''
        sha = _HASH_ALGORITHMS[algorithm]
        h = hashes.Hash(sha)
        h.update(data)
        return h.finalize()

    @classmethod
    def sign(cls, key_pair, inp, outp, args=Namespace(**{'sha':'sha256'})):
        '''Sign something with a given private key'''
        helper = SigningHelper(key_pair._private_key.curve) # pylint: disable=protected-access
        m = inp.read()
        h_1 = helper.hash(args.sha, m.encode('utf-8'))
        h_2 = helper.hash(args.sha, b''.join([h_1, m.encode('utf-8')]))
        prime_keypair = helper.keypair_from_hash(h_1)
        k = key_pair._private_key.exchange(ec.ECDH(), prime_keypair._public_key) # pylint: disable=protected-access
        hkdf = HKDF(
            algorithm=_HASH_ALGORITHMS[args.sha],
            length=32,
            salt=h_2,
            info=None
            )
        s = hkdf.derive(k)
        hmac = HMAC(key=s, algorithm=_HASH_ALGORITHMS[args.sha])
        hmac.update(m.encode('utf-8'))
        m_prime = hmac.finalize()
        if outp:
            outp.writelines([f'sha={args.sha}\n', f'mac={str(base64.b64encode(m_prime), encoding="utf-8")}\n'])
        return m_prime

    @classmethod
    def verify(cls, public_key, data, signature):
        '''Verify a signature'''
        for line in signature.readlines():
            s = line.split('=', 1)
            if s[0] == 'sha':
                sha = s[1].replace('\n', '')
            elif s[0] == 'mac':
                mac = base64.b64decode(s[1])
            else:
                print(f'Unknown line type {s[0]}, ignoring', file=sys.stderr)
        helper = SigningHelper(public_key._public_key.curve) # pylint: disable=protected-access
        m = data.read()
        h_1 = helper.hash(sha, m.encode('utf-8'))
        h_2 = helper.hash(sha, b''.join([h_1, m.encode('utf-8')]))
        prime_keypair = helper.keypair_from_hash(h_1)
        k_prime = prime_keypair._private_key.exchange(ec.ECDH(), public_key._public_key) # pylint: disable=protected-access
        hkdf = HKDF(
            algorithm=_HASH_ALGORITHMS[sha],
            length=32,
            salt=h_2,
            info=None
            )
        s_prime = hkdf.derive(k_prime)
        hmac = HMAC(key=s_prime, algorithm=_HASH_ALGORITHMS[sha])
        hmac.update(m.encode('utf-8'))
        m_prime = hmac.finalize()
        return mac == m_prime
