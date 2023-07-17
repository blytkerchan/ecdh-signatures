'''ECDH signatures implementation'''
from argparse import Namespace
from ._constants import CURVES as _CURVES
from ._signing_helper import SigningHelper

def generate(curve):
    '''Generate a keypair'''
    _curve = _CURVES[curve] # pylint: disable=invalid-name
    return SigningHelper(_curve).generate_keypair()

def sign(key_pair, inp, sha='sha256'):
    '''Sign something'''
    return SigningHelper.sign(key_pair, inp, outp=None, args=Namespace(sha=sha))

def verify(public_key, inp, signature, sha='sha256'):
    '''Verify a given signature'''
    return SigningHelper.verify(public_key, inp, signature, sha)
