'''Constants for use in the module'''
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

CURVES = {
    'prime192v1': ec.SECP192R1(),
    'prime256v1': ec.SECP256R1(),
    'secp192r1': ec.SECP192R1(),
    'secp224r1': ec.SECP224R1(),
    'secp256r1': ec.SECP256R1(),
    'secp384r1': ec.SECP384R1(),
    'secp521r1': ec.SECP521R1(),
    'secp256k1': ec.SECP256K1(),
    'sect163k1': ec.SECT163K1(),
    'sect233k1': ec.SECT233K1(),
    'sect283k1': ec.SECT283K1(),
    'sect409k1': ec.SECT409K1(),
    'sect571k1': ec.SECT571K1(),
    'sect163r2': ec.SECT163R2(),
    'sect233r1': ec.SECT233R1(),
    'sect283r1': ec.SECT283R1(),
    'sect409r1': ec.SECT409R1(),
    'sect571r1': ec.SECT571R1(),
    'brainpoolP256r1': ec.BrainpoolP256R1(),
    'brainpoolP384r1': ec.BrainpoolP384R1(),
    'brainpoolP512r1': ec.BrainpoolP512R1(),
    }

HASH_ALGORITHMS = {
    'sha1': hashes.SHA1(),
    'sha512-224': hashes.SHA512_224(),
    'sha512-256': hashes.SHA512_256(),
    'sha224': hashes.SHA224(),
    'sha256': hashes.SHA256(),
    'sha384': hashes.SHA384(),
    'sha512': hashes.SHA512(),
    'sha3-224': hashes.SHA3_224(),
    'sha3-256': hashes.SHA3_256(),
    'sha3-384': hashes.SHA3_384(),
    'sha3-512': hashes.SHA3_512(),
    'shake128': hashes.SHAKE128(digest_size=16),
    'shake256': hashes.SHAKE256(digest_size=32),
    'md5': hashes.MD5(),
    'blake2b': hashes.BLAKE2b(digest_size=64),
    'blake2s': hashes.BLAKE2s(digest_size=32),
    'sm3': hashes.SM3(),
    }
