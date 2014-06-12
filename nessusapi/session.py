# session.py

import random

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
        self.token = self.get('login', login=user,password=pw)
    
    def get(self, path, **kwargs):
        if hasattr(self, 'token'):
            kwargs['token'] = self.token
        kwargs['seq'] = random.randrange(1000000)
        url = 'https://{0}:{1}/{2}'.format(self.host,self.port,path)
        request = Request(url, urlencode(kwargs))
        try:
            response = urlopen(request)
        except HTTPError as e:
            raise AuthenticationError
        except URLError as e:
            raise ConnectionError

class ConnectionError(Exception):
    pass

class AuthenticationError(Exception):
    pass

