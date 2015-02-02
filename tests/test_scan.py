# coding=utf-8

try:
    import unittest.mock as mock
except ImportError:
    import mock

import unittest
import nessusapi.scan

class TestScan(unittest.TestCase):
    def test_init(self):
        fake_nessus = mock.Mock(request_single=
                                mock.Mock(return_value='e3b4f63f-de03-ec8b'))

        scan = nessusapi.scan.Scan(fake_nessus,'192.0.2.9', 'TestScan', 5)
        self.assertEqual(scan.uuid, 'e3b4f63f-de03-ec8b')
        fake_nessus.request_single.assert_called_with('scan/new',
                                                'scan', 'uuid',
                                                target='192.0.2.9',
                                                scan_name='TestScan',
                                                policy_id=5)

if __name__ == '__main__':
    unittest.main()
