'''Command line tool for ecdh signatures'''
# pylint: disable=invalid-name
import argparse
import sys
from ._signing_helper import SigningHelper
from ._constants import CURVES as _CURVES
from ._constants import HASH_ALGORITHMS as _HASH_ALGORITHMS
from .public_key import PublicKey
from .key_pair import KeyPair

def extract(args):
    '''Extract a public key and save it'''
    try:
        key_pair = KeyPair.load(args.keyfile, args.password)
    except ValueError as e:
        print(e.message)
        sys.exit(1)
    with open(args.output, 'x', encoding='utf-8') if args.output != '-' else sys.stdout as outp:
        key_pair.public_key().save(outp)

def generate(args):
    '''Generate a keypair'''
    curve = _CURVES[args.curve]
    key_pair = SigningHelper(curve).generate_keypair()
    key_pair.save(args.keyfile, args.password)

def sign(args):
    '''Sign something'''
    try:
        key_pair = KeyPair.load(args.keyfile, args.password)
    except ValueError as e:
        print(e.message)
        sys.exit(1)
    with open(
        args.filename, encoding='utf-8'
        ) if args.filename != '-' else sys.stdin as inp, open(
        args.output, 'x', encoding='utf-8'
        ) if args.output != '-' else sys.stdout as outp:
        SigningHelper.sign(key_pair, inp, outp, args)

def verify(args):
    '''Verify the signature on something'''
    with open(args.pubkeyfile, 'r', encoding='utf-8') as pubkeyfile:
        public_key = PublicKey.load(pubkeyfile)
    with open(
        args.filename,
        'r',
        encoding='utf-8') if args.filename != '-' else sys.stdin as f, open(
            args.signature,
            'r',
            encoding='utf-8'
            ) as s:
        sys.exit(0 if SigningHelper.verify(public_key, f, s) else 1)

parser = argparse.ArgumentParser(
                    prog='ecdh_signatures',
                    description='Implements the ECDH signature protocol',
                    )
subparsers = parser.add_subparsers(required=True)
# extract command arguments
extractparser = subparsers.add_parser('extract')
extractparser.add_argument(
    '-k',
    '--keyfile',
    help='File to read the private key from',
    action='store',
    type=str,
    required=True
    )
extractparser.add_argument(
    '-p',
    '--password',
    help='Password to be used for keyfile',
    action='store',
    type=str,
    required=True
    )
extractparser.add_argument(
    '-o',
    '--output',
    help='Output file for the public key',
    action='store',
    type=str,
    required=False,
    default='-'
    )
extractparser.set_defaults(func=extract)
# Generate command arguments
genparser = subparsers.add_parser('generate')
genparser.add_argument(
    '-c',
    '--curve',
    help='Curve to use',
    action='store',
    choices=_CURVES.keys(),
    default='secp256k1',
    )
genparser.add_argument(
    '-k',
    '--keyfile',
    help='File to store the private key',
    action='store',
    type=str,
    required=True
    )
genparser.add_argument(
    '-p',
    '--password',
    help='Password to be used for keyfile',
    action='store',
    type=str,
    required=True
    )
genparser.set_defaults(func=generate)
# sign command arguments
signparser = subparsers.add_parser('sign')
signparser.add_argument(
    '-k',
    '--keyfile',
    help='File to read the private key from',
    action='store',
    type=str,
    required=True
    )
signparser.add_argument(
    '-p',
    '--password',
    help='Password to be used for keyfile',
    action='store',
    type=str,
    required=True
    )
signparser.add_argument(
    '-f',
    '--filename',
    help='File to generate a signature for (stdin by default)',
    action='store',
    type=str,
    required=False,
    default='-'
    )
signparser.add_argument(
    '-o',
    '--output',
    help='Output file for (detached) signature (stdout by default)',
    action='store',
    type=str,
    required=False,
    default='-'
    )
signparser.add_argument(
    '-s',
    '--sha',
    help='Secure hash algorithm to use for the signature generation',
    action='store',
    type=str,
    required=False,
    default='sha256',
    choices=_HASH_ALGORITHMS.keys()
    )
signparser.set_defaults(func=sign)
# verify command arguments
verifyparser = subparsers.add_parser('verify')
verifyparser.add_argument(
    '-p',
    '--pubkeyfile',
    help='File to read the public key from',
    action='store',
    type=str,
    required=True
    )
verifyparser.add_argument(
    '-f',
    '--filename',
    help='File to verify a signature for (stdin by default)',
    action='store',
    type=str,
    required=False,
    )
verifyparser.add_argument(
    '-s',
    '--signature',
    help='File containing the (detached) signature',
    action='store',
    type=str,
    required=True,
    )
verifyparser.set_defaults(func=verify)

parsed_args = parser.parse_args(args=sys.argv[1:])
parsed_args.func(parsed_args)
