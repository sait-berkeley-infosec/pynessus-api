#!/usr/bin/env python
# coding=utf-8

try:
    import unittest.mock as mock
except ImportError:
    import mock

import unittest
import nessusapi.nessus

class TestNessus(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.real_session = nessusapi.nessus.Session
        nessusapi.nessus.Session = mock.Mock()

    @classmethod
    def tearDownClass(cls):
        nessusapi.nessus.Session = cls.real_session

    def test_init(self):
        mock_session = nessusapi.nessus.Session
        nessusapi.nessus.Nessus('user', 'pw')
        mock_session.assert_called_with('user', 'pw', host='localhost',
                                        port=8834, verifySSL=True)

        nessusapi.nessus.Nessus('user', 'pw', port=80)
        mock_session.assert_called_with('user', 'pw', host='localhost',
                                        port=80, verifySSL=True)

        nessusapi.nessus.Nessus('user', 'pw', 'host', 30, False)
        mock_session.assert_called_with('user', 'pw', host='host',
                                        port=30, verifySSL=False)


    @mock.patch('nessusapi.nessus.Nessus.request_list')
    def test_reports(self, mock_request_list):
        nessus = nessusapi.nessus.Nessus('user', 'pw')

        mock_request_list.return_value = []
        reports = nessus.reports
        self.assertEqual(reports, [])
        mock_request_list.assert_called_with('report/list', 'reports',
                                             'report')

        mock_request_list.return_value = [{'name': '123-ab', 'timestamp': '5',
                                           'readableName': 'report1',
                                           'status': 'completed'}]
        reports = nessus.reports
        self.assertEqual(len(reports), 1)
        self.assertEqual(reports[0].uuid, '123-ab')
        self.assertEqual(reports[0].timestamp, 5)
        self.assertEqual(reports[0].name, 'report1')
        self.assertEqual(reports[0].status, 'completed')

        mock_request_list.return_value = [{'name': '321-ba', 'timestamp': '5',
                                           'readableName': 'report2',
                                           'status': 'completed'},
                                          {'name': '456-de', 'timestamp': '21',
                                           'readableName': 'report3',
                                           'status': 'stopped'}]

        reports = nessus.reports
        self.assertEqual(len(reports), 2)


