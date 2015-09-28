"""
The majority of this code was taken from secure scaffold framework
"""

import hashlib
import hmac
import time

DELIMITER = ':'
DEFAULT_TIMEOUT = 86400


def compare(a, b):
    """ Compares a and b in constant time and returns True if they are equal. """
    if len(a) != len(b):
        return False
    result = 0
    for x, y in zip(a, b):
        result |= ord(x) ^ ord(y)

    return result == 0


def generate_token(key, user, action='*', now=None):
    """ Generates an XSRF token for the provided user and action. """
    token_timestamp = now or int(time.time())
    message = DELIMITER.join([user, action, str(token_timestamp)])
    digest = hmac.new(key, message, hashlib.sha1).hexdigest()
    return DELIMITER.join([str(token_timestamp), digest])


def validate_token(key, user, token, action='*', max_age=DEFAULT_TIMEOUT):
    """Validates the provided XSRF token."""
    if not token or not user:
        return False
    try:
        (timestamp, digest) = token.split(DELIMITER)
    except ValueError:
        return False
    expected = generate_token(key, user, action, timestamp)
    (_, expected_digest) = expected.split(DELIMITER)
    now = int(time.time())
    if compare(expected_digest, digest) and now < int(timestamp) + max_age:
        return True
    return False
