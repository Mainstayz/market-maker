from requests.auth import AuthBase
import time
import hashlib
import hmac
import base64
from urllib.parse import urlparse
import datetime


class APIKeyAuthOkexV3(AuthBase):
    """Attaches API Key Authentication to the given Request object."""

    def __init__(self, apiKey, apiSecret, passPhrase, iso, epoch):
        """Init with Key & Secret & passPhrase."""
        self.apiKey = apiKey
        self.apiSecret = apiSecret
        self.passPhrase = passPhrase
        self.iso = iso
        self.epoch = epoch

    def __call__(self, r):
        """Called when forming a request - generates api key headers."""
        # modify and return the request

        milli = generate_nonce_milli() + 2000

        epoch = generate_epoch_milli(milli)

        iso = datetime.datetime.fromtimestamp(epoch/1000).isoformat()

        r.headers['OK-ACCESS-TIMESTAMP'] = self.epoch
        r.headers['OK-ACCESS-KEY'] = self.apiKey
        r.headers['OK-ACCESS-SIGN'] = generate_signature(self.iso, r.method, r.url, r.body or '', self.apiSecret)
        r.headers['OK-ACCESS-PASSPHRASE'] = self.passPhrase
        return r


def generate_nonce_milli():
    return int(round((time.time() + 3600 )* 1000))


def generate_epoch_milli(m):
    return m - 28800000


def generate_signature(iso, method, url, body, secret):
    parsedURL = urlparse(url)
    path = parsedURL.path

    if parsedURL.query:
        path = path + '?' + parsedURL.query

    if isinstance(body, (bytes, bytearray)):
        body = body.decode('utf8')

    message = iso + method + path + body
    print(message)
    signature = hmac.new(bytes(secret, 'utf8'), bytes(message, 'utf8'), digestmod=hashlib.sha256).hexdigest()

    encodestr = base64.b64encode(bytes(signature, 'utf8'))

    return str(encodestr, 'utf8')


if __name__ == "__main__":
    print(time.time())
