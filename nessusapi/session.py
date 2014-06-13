# session.py

import random
import xmltodict

# try python 3 imports, fall back to python 2
try:
    from urllib.parse import urlencode
    from urllib.request import urlopen, Request
    from urllib.error import URLError, HTTPError
except ImportError:
    from urllib import urlencode
    from urllib2 import urlopen, Request, URLError, HTTPError

class Session:
    def __init__(self, user, pw, host='localhost', port=8834):
        self.host = host
        self.port = port

    def __enter__(self):
        self.token = self.get('login', login=user,password=pw)['token']

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self.get('logout')['contents'] == 'OK'
    
    def get(self, path, **kwargs):
        if 'token' not in kwargs and hasattr(self, 'token'):
            kwargs['token'] = self.token
        kwargs['seq'] = random.randrange(1000000)
        url = 'https://{0}:{1}/{2}'.format(self.host,self.port,path)
        request = Request(url, urlencode(kwargs))
        try:
            response = urlopen(request)
            response_data = xmltodict.parse(response.read())
            if response_data['seq'] != kwargs['seq']:
                raise Exception("Unique number did not match!")
            elif response_data['status'] != 'OK':
                raise AuthenticationError("Invalid credentials")
            return response_data
        except HTTPError as e:
            raise AuthenticationError
        except URLError as e:
            raise ConnectionError

class ConnectionError(Exception):
    pass

class AuthenticationError(Exception):
    pass

