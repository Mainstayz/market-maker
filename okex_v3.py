from __future__ import absolute_import
from auth.APIKeyAuthOkexV3 import *
import requests
import time
import datetime
import base64
import uuid
import json

proxies = {
    "http": "http://127.0.0.1:8001",
    "https": "http://127.0.0.1:8001",
}


class Okex_v3(object):
    def __init__(self, apiKey=None, apiSecret=None, passPhrase=None,
                 orderIDPrefix='zz_okex_', shouldWSAuth=True, postOnly=False, timeout=7):
        self.baseUrl = 'https://www.okex.com'
        self.apiKey = apiKey
        self.apiSecret = apiSecret
        self.passPhrase = passPhrase
        self.orderIDPrefix = orderIDPrefix
        self.shouldWSAuth = shouldWSAuth
        self.postOnly = postOnly
        self.timeout = timeout
        # initialize counter
        self.retries = 0

        self.session = requests.Session()
        # These headers are always sent
        self.session.headers.update({'content-type': 'application/json'})
        self.session.headers.update({'accept': 'application/json'})

    def curl(self, path, query=None, postdict=None, timeout=None, verb=None, rethrow_errors=False,
             max_retries=None):
        # Handle URL
        url = self.baseUrl + path

        if timeout is None:
            timeout = self.timeout

        if not verb:
            verb = 'POST' if postdict else 'GET'

        if max_retries is None:
            max_retries = 0 if verb in ['POST', 'PUT'] else 3

        server_time_url = self.baseUrl + '/api/general/v3/time'
        server_time = requests.request(url=server_time_url, method='GET', proxies=proxies, timeout=timeout).json()

        auth = APIKeyAuthOkexV3(self.apiKey, self.apiSecret, self.passPhrase, server_time['iso'], server_time['epoch'])

        def exit_or_throw(e):
            if rethrow_errors:
                raise e
            else:
                exit(1)

        def retry():
            self.retries += 1
            if self.retries > max_retries:
                raise Exception("Max retries on %s (%s) hit, raising." % (path, json.dumps(postdict or '')))
            return self.curl(path, query, postdict, timeout, verb, rethrow_errors, max_retries)

        # Make the request
        response = None

        try:
            print(("sending req to %s: %s" % (url, json.dumps(postdict or query or ''))))
            req = requests.Request(verb, url, json=postdict, auth=auth, params=query)
            prepped = self.session.prepare_request(req)
            print(prepped.headers)
            response = self.session.send(prepped, proxies=proxies, timeout=timeout)
            # Make non-200s throw
            response.raise_for_status()

        except requests.exceptions.HTTPError as e:

            if response is None:
                raise e
            print(response.status_code)
            print(response.content)
            return retry()

        except requests.exceptions.Timeout as e:
            # Timeout, re-run this request
            print("Timed out on request: %s (%s), retrying..." % (path, json.dumps(postdict or '')))
            return retry()

        except requests.exceptions.ConnectionError as e:
            print("Unable to contact the OKEX API (%s). Please check the URL. Retrying. " + "Request: %s %s \n %s" % (
                e, url, json.dumps(postdict)))
            time.sleep(1)
            return retry()

            # Reset retry counter on success
        self.retries = 0

        return response.json()


if __name__ == "__main__":
    okex = Okex_v3('68d3ba44-9531-4dbf-a395-25e8689252f5', '87BD81325D7073E4FE8C5B31973E6656', 'caibudao0701')
    response = okex.curl('/api/account/v3/currencies')
