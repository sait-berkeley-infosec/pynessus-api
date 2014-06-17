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
        self.token = self.request('login', login=user,password=pw)['token']

    def close(self):
        return self.request('logout') == 'OK'
    
    def request(self, path, token=None, **kwargs):
        if token:
            kwargs['token'] = self.token
        kwargs['seq'] = random.randrange(1000000)
        url = 'https://{0}:{1}/{2}'.format(self.host,self.port,path)
        request = Request(url, urlencode(kwargs))
        try:
            response = urlopen(request)
            response_data = xmltodict.parse(response.read())['reply']
            if int(response_data['seq']) != kwargs['seq']:
                raise Exception("Unique number did not match!")
            elif response_data['status'] != 'OK':
                raise AuthenticationError("Invalid credentials")
            return response_data['contents']
        except HTTPError as e:
            raise AuthenticationError
        except URLError as e:
            raise ConnectionError

class ConnectionError(Exception):
    pass

class AuthenticationError(Exception):
    pass

