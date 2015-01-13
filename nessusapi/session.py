import random
# try python 3 imports, fall back to python 2

import requests
import xmltodict

class Session:
    current = None
    def __init__(self, user, pw, host='localhost', port=8834, verifySSL=True):
        """Create a session and make it the active one"""
        self.host = host
        self.port = port
        self.token = self.request('login', verifySSL=verifySSL,
                                  login=user, password=pw)['token']
        Session.current = self

    def close(self):
        """Log out of the API and invalidate the token"""
        if self.request('logout') == 'OK':
            self.token = None
            return True
        return False
    
    def request(self, path, verifySSL=True, **kwargs):
        """Make a request to a path with specified kwargs"""
        if hasattr(self, 'token'):
            kwargs['token'] = self.token 

        url = 'https://{0}:{1}/{2}'.format(self.host,self.port,path)
        r = requests.post(url, verify=verifySSL, data=kwargs)
        if r.status_code != requests.codes.ok:
            raise r.raise_for_status()

        response_data = xmltodict.parse(r.text)['reply']
        if response_data['status'] != 'OK':
            raise AuthenticationError("Invalid credentials")
        return response_data['contents']

def request(path, **kwargs):
    return Session.current.request(path, **kwargs)

class ConnectionError(Exception):
    pass

class AuthenticationError(Exception):
    pass

