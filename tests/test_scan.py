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

from nessusapi.scan import Scan
from nessusapi.session import Session

class SessionTestCase(unittest.TestCase):
    def test_init(self):
        fake_session = mock.MagicMock(Session)
        fake_session.request.return_value = {'uuid': 'e3b4f63f-de03-ec8b'}
        scan = Scan('192.0.2.9', 'TestScan', '5', fake_session)
        self.assertEqual(scan.uuid, 'e3b4f63f-de03-ec8b')
        fake_session.request.assert_called_with('scan/new',
                                                target='192.0.2.9',
                                                scan_name='TestScan',
                                                policy_id='5')

if __name__ == '__main__':
    unittest.main()
