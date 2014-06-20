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
    current = None
    def __init__(self, user, pw, host='localhost', port=8834):
        self.host = host
        self.port = port
        self.token = self.request('login', login=user,password=pw)['token']
        Session.current = self

    def close(self):
        if self.request('logout') == 'OK':
            self.token = None
            return True
        return False
    
    def request(self, path, **kwargs):
        if hasattr(self, 'token'):
            kwargs['token'] = self.token 
        url = 'https://{0}:{1}/{2}'.format(self.host,self.port,path)
        request = Request(url, urlencode(kwargs))
        try:
            response = urlopen(request)
            response_data = xmltodict.parse(response.read())['reply']
            if response_data['status'] != 'OK':
                raise AuthenticationError("Invalid credentials")
            return response_data['contents']
        except HTTPError as e:
            raise AuthenticationError
        except URLError as e:
            raise ConnectionError

def require_auth(f):
    def with_auth(self, *args, **kwargs):
        self.session = Session.current
        return f(self, *args, **kwargs)
    return with_auth
    

class ConnectionError(Exception):
    pass

class AuthenticationError(Exception):
    pass

