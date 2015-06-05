#!/usr/bin/env python
# coding=utf-8

import mock
import pytest
from requests.exceptions import ConnectionError

import nessusapi.session
from api_responses import (
    mock_response,
    mock_failed_request,
    xml_login_success,
    xml_login_error,
    xml_logout_success,
)


class TestSession():
    @mock.patch('nessusapi.session.requests.post')
    def test_init(self, mock_post):
        mock_post.return_value = mock_response(xml_login_success)

        s = nessusapi.session.Session("user", "pwd", "host", 8834)

        mock_post.assert_called_once_with("https://host:8834/login",
                                          verify=True,
                                          data={"login": "user",
                                                "password": "pwd",
                                                "token": None})

        assert s.token == 'abcdef01'
        assert s.host == 'host'
        assert s.port == 8834

    @mock.patch('nessusapi.session.requests.post')
    def test_request_bad_login(self, mock_post):
        mock_post.return_value = mock_response(xml_login_error)
        with pytest.raises(nessusapi.session.AuthenticationError):
            nessusapi.session.Session("user", "pwd", "host", 8834)

    @mock.patch('nessusapi.session.requests.post')
    def test_close(self, mock_post):
        mock_post.return_value = mock_response(xml_login_success)
        s = nessusapi.session.Session("user", "pwd", "host", 8834)

        assert s.token is not None
        token = s.token

        mock_post.return_value = mock_response(xml_logout_success)
        assert s.close() is True
        assert s.token is None
        mock_post.assert_called_with("https://host:8834/logout",
                                     verify=True,
                                     data={"token": token})

        with pytest.raises(nessusapi.session.AuthenticationError):
            s.close()

    @mock.patch('nessusapi.session.requests.post')
    def test_request_failure(self, mock_post):
        mock_post.return_value = mock_failed_request(status=403)
        with pytest.raises(ConnectionError):
            nessusapi.session.Session("user", "pwd", "host", 8834)

        mock_post.return_value = mock_failed_request(status=501)
        with pytest.raises(ConnectionError):
            nessusapi.session.Session("user", "pwd", "host", 8834)
