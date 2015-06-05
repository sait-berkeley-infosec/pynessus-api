#!/usr/bin/env python
# coding=utf-8

import mock

import nessusapi.nessus


class TestNessus():
    @mock.patch('nessusapi.nessus.Session')
    def test_init(self, mock_session):
        nessusapi.nessus.Nessus('user', 'pw')
        mock_session.assert_called_with('user', 'pw', host='localhost',
                                        port=8834, verifySSL=True)

        nessusapi.nessus.Nessus('user', 'pw', port=80)
        mock_session.assert_called_with('user', 'pw', host='localhost',
                                        port=80, verifySSL=True)

        nessusapi.nessus.Nessus('user', 'pw', 'host', 30, False)
        mock_session.assert_called_with('user', 'pw', host='host',
                                        port=30, verifySSL=False)

    @mock.patch('nessusapi.nessus.Session')
    def test_logout(self, mock_session):
        nessus = nessusapi.nessus.Nessus('user', 'pw')
        nessus.logout()

        assert mock.call('user', 'pw', host='localhost', verifySSL=True, port=8834) in mock_session.mock_calls

    @mock.patch('nessusapi.nessus.Nessus.request_list')
    @mock.patch('nessusapi.nessus.Session')
    def test_reports(self, mock_session, mock_request_list):
        nessus = nessusapi.nessus.Nessus('user', 'pw')

        mock_request_list.return_value = []
        assert nessus.reports == []

        mock_request_list.assert_called_with('report/list', 'reports',
                                             'report')

        mock_request_list.return_value = [{'name': '123-ab', 'timestamp': '5',
                                           'readableName': 'report1',
                                           'status': 'completed'}]
        reports = nessus.reports
        assert len(reports) == 1
        assert reports[0].uuid == '123-ab'
        assert reports[0].timestamp == 5
        assert reports[0].name == 'report1'
        assert reports[0].status == 'completed'

        mock_request_list.return_value = [{'name': '321-ba', 'timestamp': '5',
                                           'readableName': 'report2',
                                           'status': 'completed'},
                                          {'name': '456-de', 'timestamp': '21',
                                           'readableName': 'report3',
                                           'status': 'stopped'}]

        reports = nessus.reports
        assert len(reports) == 2
