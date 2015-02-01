#!/usr/bin/env python
# coding=utf-8

try:
    import unittest.mock as mock
except ImportError:
    import mock

import unittest
import nessusapi.session

xml_login_success = ('<?xml version="1.0"?> <reply>'
                     "<status>OK</status>"
                     "<contents><token>abcdef01</token>"
                     "<user>"
                     "<name>admin</name>"
                     "<admin>TRUE</admin>"
                     "</user></contents>"
                     "</reply>")

xml_login_error   = ('<?xml version="1.0"?> <reply>'
                     "<status>ERROR</status>"
                     "<contents>Invalid login</contents>"
                     "</reply>")

class TestSession(unittest.TestCase):
    @mock.patch('nessusapi.session.Session.request')
    def test_init(self, mock_request):
        mock_request.return_value = {'token': 'test_token'}

        s = nessusapi.session.Session("user", "pwd", "host", 8834)

        mock_request.assert_called_once_with("login",**{"login":"user",
                                                        "password": "pwd"})

        self.assertEqual(s.token, 'test_token')
        self.assertEqual(s.host, 'host')
        self.assertEqual(s.port, 8834)

    @mock.patch('nessusapi.session.Session.request')
    def test_close(self, mock_request):
        from nessusapi.session import AuthenticationError 
        mock_request.return_value = {'token': 'test_token'}
        s = nessusapi.session.Session("user", "pwd", "host", 8834)
        self.assertIsNotNone(s.token)
        
        mock_request.return_value = "OK"
        self.assertTrue(s.close())
        self.assertIsNone(s.token)
        mock_request.assert_called_with("logout")

        self.assertRaises(AuthenticationError, s.close)

    @mock.patch('nessusapi.session.requests.post')
    def test_request_failure(self, mock_post):
        from requests.exceptions import ConnectionError
        def _raise(ex):
            raise ex

        mock_post.return_value=mock.Mock(status_code=403,
                                         raise_for_status=lambda: _raise(ConnectionError))
        self.assertRaises(ConnectionError, nessusapi.session.Session,
                          *("user", "pwd", "host", 8834))

        mock_post.return_value=mock.Mock(status_code=501,
                                         raise_for_status=lambda: _raise(ConnectionError))
        self.assertRaises(ConnectionError, nessusapi.session.Session,
                          *("user", "pwd", "host", 8834))

    @mock.patch('nessusapi.session.requests.post')
    def test_request_bad_login(self, mock_post):
        from nessusapi.session import AuthenticationError 
        mock_post.return_value=mock.Mock(status_code=200,
                                         raise_for_status=lambda: None,
                                         text=xml_login_error)
        self.assertRaises(AuthenticationError, nessusapi.session.Session,
                          *("user", "pwd", "host", 8834))

