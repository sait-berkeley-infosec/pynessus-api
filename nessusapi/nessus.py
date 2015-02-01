import os
import xmltodict

from nessusapi.session import Session
from nessusapi.report import Host, Report
from nessusapi.vulnerability import Vulnerability

class Nessus(object):
    def __init__(self, user, pw, host='localhost', port=8834, verifySSL=True):
        """Create a session and make it the active one"""
        self.session = Session(user, pw, host=host, port=port, verifySSL=verifySSL)

    @classmethod
    def from_env(cls):
        # os.environ throws an error if the key is not present
        user = os.environ['NESSUS_USERNAME']
        pw   = os.environ['NESSUS_PASSWORD']
        # os.getenv does not throw errors, and allows for a default value
        host = os.getenv('NESSUS_HOST', 'localhost')
        port = os.getenv('NESSUS_PORT', 8834)
        verifySSL = os.getenv('NESSUS_VERIFYSSL', True)

        return cls(user, pw, host=host, port=port, verifySSL=verifySSL)

    def logout(self):
        """Log out of the API and invalidate the token"""
        self.session.close()
    
    @property
    def reports(self):
        raw_list = self.request_list('report/list', 'reports', 'report')

        reports = []
        for report in raw_list:
            r = Report(nessus=self, uuid=report['name'])
            r.timestamp = int(report['timestamp'])
            r.status = report['status']
            r.name = report['readableName']
            reports.append(r)
        
        return reports

    def _host_details(self, report, host):
        tcp_list = request_list(self._request('report/details', report=report.uuid, hostname=host.hostname, protocol='tcp')['portDetails']['ReportItem'])
        udp_list = request_list(self._request('report/details', report=report.uuid, hostname=host.hostname, protocol='udp')['portDetails']['ReportItem'])
        return tcp_list + udp_list

    def _request(self, path, **kwargs):
        return self.session.request(path, **kwargs)

    def request_list(self, path, *keys, **kwargs):
        try:
            request = self._request(path, **kwargs)
            for key in keys:
                request = request[key]
            return _ensure_list(request)
        except TypeError:
            return []

# requests sometimes do not return lists, so use this to make them lists
def _ensure_list(obj):
    if not isinstance(obj, list):
        return [obj]
    return obj

class ConnectionError(Exception):
    pass

class AuthenticationError(Exception):
    pass

