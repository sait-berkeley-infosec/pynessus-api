import mock
from requests.exceptions import ConnectionError


def raise_(ex):
    raise ex


def mock_response(response):
    return mock.Mock(status_code=200, text=response)


def mock_failed_request(status, exception=ConnectionError):
    return mock.Mock(status_code=status,
                     raise_for_status=lambda: raise_(ConnectionError))

xml_login_success = ('<?xml version="1.0"?> <reply>'
                     "<status>OK</status>"
                     "<contents><token>abcdef01</token>"
                     "<user>"
                     "<name>admin</name>"
                     "<admin>TRUE</admin>"
                     "</user></contents>"
                     "</reply>")

xml_login_error = ('<?xml version="1.0"?> <reply>'
                   "<status>ERROR</status>"
                   "<contents>Invalid login</contents>"
                   "</reply>")

xml_logout_success = ('<?xml version="1.0" encoding="UTF-8"?> <reply>'
                      '<status>OK</status>'
                      '<contents>OK</contents>'
                      '</reply>')
