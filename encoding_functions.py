from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.x509 import CertificateSigningRequestBuilder
from cryptography.x509.oid import NameOID
from cryptography import x509
import string
from utilitybelt import int_to_charset, charset_to_int
from secretsharing.sharing import point_to_share_string, share_string_to_point
from secretsharing.polynomials import get_polynomial_points, modular_lagrange_interpolation
import sys


def generate_rsa_key_and_public_key(bits: int = 4096):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=bits,
        backend=default_backend())

    csr = CertificateSigningRequestBuilder().subject_name(
        x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, 'IT'),
            x509.NameAttribute(NameOID.LOCALITY_NAME, 'Rome'),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'Colossus'),
            x509.NameAttribute(NameOID.COMMON_NAME, 'colossus.digital'),
            x509.NameAttribute(NameOID.EMAIL_ADDRESS, '')])
    ).sign(private_key, hashes.SHA256(), default_backend())

    public = csr.public_bytes(serialization.Encoding.PEM)
    private = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption())
    return public.decode('utf-8'), private.decode('utf-8')


def split_and_encode_string(secret_string, k=2, n=4, chunk_size=1024):
    # Split the large string into smaller chunks
    secret_chunks = _split_large_string(secret_string, chunk_size)
    # Split each chunk into shares
    share_chunks = []
    for chunk in secret_chunks:
        hex_chunk = string_to_hex(chunk)
        shares = PlaintextToHexSecretSharer.split_secret(hex_chunk, k, n)
        share_chunks.append(shares)
    return share_chunks


def combine_secret_shares(share_chunks):
    if len(share_chunks) > 1:
        if share_chunks[0][0][0] != share_chunks[1][0][0]:
            share_chunks = prepare_shares_for_combine(share_chunks)

    # Recover each chunk using a subset of the shares
    recovered_secret_chunks = []
    for shares in share_chunks:
        recovered_hex_chunk = PlaintextToHexSecretSharer.recover_secret(shares)
        recovered_chunk = hex_to_string(recovered_hex_chunk)
        recovered_secret_chunks.append(recovered_chunk)
    # Combine the recovered chunks to form the recovered secret string
    recovered_secret_string = "".join(recovered_secret_chunks)
    return recovered_secret_string


def prepare_shares_for_combine(shares):
    share_chunks = []
    for i in range(len(shares[0])):
        temp = []
        for j in shares:
            temp.append(j[i])
        share_chunks.append(temp)
    return share_chunks


def _split_large_string(secret_string, chunk_size):
    return [secret_string[i:i + chunk_size] for i in range(0, len(secret_string), chunk_size)]


class SecretSharer:
    """ Creates a secret sharer, which can convert from a secret string to a
        list of shares and vice versa. The splitter is initialized with the
        character set of the secrets and the character set of the shares that
        it expects to be dealing with.
    """
    secret_charset = string.hexdigits[0:16]
    share_charset = string.hexdigits[0:16]

    def __init__(self):
        pass

    @classmethod
    def split_secret(cls, secret_string, share_threshold, num_shares):
        secret_int = charset_to_int(secret_string, cls.secret_charset)
        points = secret_int_to_points(secret_int, share_threshold, num_shares)
        shares = []
        for point in points:
            shares.append(point_to_share_string(point, cls.share_charset))
        return shares

    @classmethod
    def recover_secret(cls, shares):
        points = []
        for share in shares:
            points.append(share_string_to_point(share, cls.share_charset))
        secret_int = points_to_secret_int(points)
        secret_string = int_to_charset(secret_int, cls.secret_charset)
        return secret_string


class PlaintextToHexSecretSharer(SecretSharer):
    """ Good for converting secret messages into standard hex shares.
    """
    secret_charset = string.printable
    share_charset = string.hexdigits[0:16]


def secret_int_to_points(secret_int, point_threshold, num_points, prime=None):
    """ Split a secret (integer) into shares (pair of integers / x,y coordinates).

        Sample the points of a random polynomial with the y intercept equal to
        the secret int.
    """
    if point_threshold < 2:
        raise ValueError("Threshold must be >= 2.")
    if point_threshold > num_points:
        raise ValueError("Threshold must be < the total number of points.")
    if not prime:
        prime = get_large_enough_prime([secret_int, num_points])
    if not prime:
        raise ValueError("Error! Secret is too long for share calculation!")
    coefficients = large_enough_polynomial(point_threshold - 1, secret_int, prime)
    points = get_polynomial_points(coefficients, num_points, prime)
    return points


def points_to_secret_int(points, prime=None):
    """ Join int points into a secret int.

        Get the intercept of a random polynomial defined by the given points.
    """
    if not isinstance(points, list):
        raise ValueError("Points must be in list form.")
    for point in points:
        if not isinstance(point, tuple) and len(point) == 2:
            raise ValueError("Each point must be a tuple of two values.")
        if not (isinstance(point[0], int) and
                isinstance(point[1], int)):
            raise ValueError("Each value in the point must be an int.")
    x_values, y_values = zip(*points)
    if not prime:
        prime = get_large_enough_prime(y_values)
    free_coefficient = modular_lagrange_interpolation(0, points, prime)
    secret_int = free_coefficient  # the secret int is the free coefficient
    return secret_int


def calculate_mersenne_primes():
    """ Returns all the mersenne primes with less than 500 digits.
        All primes:
        3, 7, 31, 127, 8191, 131071, 524287, 2147483647L, 2305843009213693951L,
        618970019642690137449562111L, 162259276829213363391578010288127L,
        170141183460469231731687303715884105727L,
        68647976601306097149...12574028291115057151L, (157 digits)
        53113799281676709868...70835393219031728127L, (183 digits)
        10407932194664399081...20710555703168729087L, (386 digits)
    """
    mersenne_prime_exponents = [
        2, 3, 5, 7, 13, 17, 19, 31, 61, 89,
        107, 127, 521, 607, 1279, 2203, 2281, 3217, 4253, 4423,
        9689, 9941, 11213, 19937, 21701]
    primes = []
    for exp in mersenne_prime_exponents:
        prime = 1
        for i in range(exp):
            prime *= 2
        prime -= 1
        primes.append(prime)
    return primes


SMALLEST_257BIT_PRIME = (2**256 + 297)
SMALLEST_321BIT_PRIME = (2**320 + 27)
SMALLEST_385BIT_PRIME = (2**384 + 231)
STANDARD_PRIMES = calculate_mersenne_primes() + [
    SMALLEST_257BIT_PRIME, SMALLEST_321BIT_PRIME, SMALLEST_385BIT_PRIME]
STANDARD_PRIMES.sort()


def get_large_enough_prime(batch):
    """ Returns a prime number that is greater all the numbers in the batch.
    """
    # build a list of primes
    primes = STANDARD_PRIMES
    # find a prime that is greater than all the numbers in the batch
    for prime in primes:
        numbers_greater_than_prime = [i for i in batch if i > prime]
        if len(numbers_greater_than_prime) == 0:
            return prime
    return None


def large_enough_polynomial(degree, intercept, upper_bound):
    """ Generates a random polynomial with positive coefficients.
    """
    if degree < 0:
        raise ValueError('Degree must be a non-negative number.')
    coefficients = [intercept]
    #sys.set_int_max_str_digits(6500)
    for i in range(degree):
        coefficient = get_large_enough_coefficient(upper_bound, i)
        coefficients.append(coefficient)
    return coefficients


def get_large_enough_coefficient(prime, i):
    kkk = '5462458264' * 1000
    c = kkk[i*3: (i*3)+(len(str(prime))-1)]
    return int(c)


def string_to_hex(s):
    return s.encode().hex()


def hex_to_string(h):
    return bytes.fromhex(h).decode()
