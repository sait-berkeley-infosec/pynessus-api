import requests
import xmltodict

class Session(object):
    def __init__(self, user, pw, host, port, verifySSL=True):
        """Create a session and make it the active one"""
        self.host = host
        self.port = port
        self.verifySSL = verifySSL
        self.token = self.request('login', login=user, password=pw)['token']

    def close(self):
        """Log out of the API and invalidate the token"""
        if self.token is None:
            return True
        if self.request('logout') == 'OK':
            self.token = None
            return True
        return False
    
    def request(self, path, **kwargs):
        """Make a request to a path with specified kwargs"""
        if hasattr(self, 'token'):
            kwargs['token'] = self.token 

        url = 'https://{0}:{1}/{2}'.format(self.host,self.port,path)
        r = requests.post(url, verify=self.verifySSL, data=kwargs)
        if r.status_code != requests.codes.ok:
            raise r.raise_for_status()

        response_data = xmltodict.parse(r.text)['reply']
        if response_data['status'] != 'OK':
            raise AuthenticationError("Invalid credentials")
        return response_data['contents']

class ConnectionError(Exception):
    pass

class AuthenticationError(Exception):
    pass

