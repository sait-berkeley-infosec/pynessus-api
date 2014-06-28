import random
# try python 3 imports, fall back to python 2
try:
    from urllib.parse import urlencode
    from urllib.request import urlopen, Request
    from urllib.error import URLError, HTTPError
except ImportError:
    from urllib import urlencode
    from urllib2 import urlopen, Request, URLError, HTTPError

import xmltodict

class Session:
    current = None
    def __init__(self, user, pw, host='localhost', port=8834):
        """Create a session and make it the active one"""
        self.host = host
        self.port = port
        self.token = self.request('login', login=user,password=pw)['token']
        Session.current = self

    def close(self):
        """Log out of the API and invalidate the token"""
        if self.request('logout') == 'OK':
            self.token = None
            return True
        return False
    
    def request(self, path, **kwargs):
        """Make a request to a path with specified kwargs"""
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
            raise 
        except URLError as e:
            raise# ConnectionError

def request(path, **kwargs):
    return Session.current.request(path, **kwargs)

class ConnectionError(Exception):
    pass

class BadRequestError(Exception):
    pass

class AuthenticationError(Exception):
    pass

