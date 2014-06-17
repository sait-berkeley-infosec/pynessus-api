#!/usr/bin/env python
# coding=utf-8

try:
    import unittest.mock as mock
except ImportError:
    import mock
import unittest
try: 
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from nessusapi.session import Session
from nessusapi.session import Request

class SessionTestCase(unittest.TestCase):
    @mock.patch('nessusapi.session.random')
    @mock.patch('nessusapi.session.urlopen')
    @mock.patch('nessusapi.session.Request')
    def test_request(self, mock_request, mock_urlopen, mock_random):
        mock_random.randrange.return_value = 2813
        mock_urlopen.return_value = StringIO('<?xml version="1.0"?> <reply>'
                                             "<seq>2813</seq>"
                                             "<status>OK</status>"
                                             "<contents><token>abcdef01</token>"
                                             "<user>"
                                             "<name>admin</name>"
                                             "<admin>TRUE</admin>"
                                             "</user></contents>"
                                             "</reply>")
        session = Session('user', 'pass', '192.0.2.7', '8981')
        mock_urlopen.return_value = StringIO('<?xml version="1.0"?> <reply>'
                                             "<seq>2813</seq>"
                                             "<status>OK</status>"
                                             "<contents>OK</contents>"
                                             "</reply>")
        session.request('test/url', arg1="arg1value", arg2="arg2value")
        mock_request.assert_called_with('https://192.0.2.7:8981/test/url',
                                        'arg1=arg1value&arg2=arg2value'
                                        '&token=abcdef01&seq=2813')

    @mock.patch('nessusapi.session.random')
    @mock.patch('nessusapi.session.urlopen')
    @mock.patch('nessusapi.session.Request')
    def test_auth(self, mock_request, mock_urlopen, mock_random):
        mock_random.randrange.return_value = 2811
        mock_urlopen.return_value = StringIO('<?xml version="1.0"?> <reply>'
                                             "<seq>2811</seq>"
                                             "<status>OK</status>"
                                             "<contents><token>ce65ea7</token>"
                                             "<user>"
                                             "<name>admin</name>"
                                             "<admin>TRUE</admin>"
                                             "</user></contents>"
                                             "</reply>")
        session = Session('user', 'pass', '192.0.2.3', '8980')
        mock_request.assert_called_once_with('https://192.0.2.3:8980/login',
                                        'login=user&password=pass&seq=2811')
        self.assertEqual(session.token, "ce65ea7")

        mock_random.randrange.return_value = 2817
        mock_urlopen.return_value = StringIO('<?xml version="1.0"?> <reply>'
                                             "<seq>2817</seq>"
                                             "<status>OK</status>"
                                             "<contents>OK</contents>"
                                             "</reply>")
        self.assertTrue(session.close())
        mock_request.assert_called_with('https://192.0.2.3:8980/logout',
                                        'token=ce65ea7&seq=2817')
        self.assertIsNone(session.token)

if __name__ == '__main__':
    unittest.main()
