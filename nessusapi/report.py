# coding=utf-8

import time

from .utils import multiton
from .vulnerability import Vulnerability

@multiton
class Report(object):
    def __init__(self, nessus, uuid):
        self.nessus = nessus
        self.uuid = uuid

        self.timestamp = None
        self.name = None

        self._status = None
        self._completed = False # lets us know if the caches need to be updated

        # Caches
        self.hosts_list = [] 
        self.vulns_list = []
    
    @property
    def status(self):
        if self._status != 'completed':
            self.nessus.reports # force cache update
        return self._status

    @status.setter
    def status(self, value):
        if self._status != 'completed' and value == 'completed':
            # Invalidate the caches
            self._completed = True
            self.hosts_list = None
            self.vulns_list = None 

        self._status = value

    @property
    def hosts(self):
        if not self.hosts_list or not self._completed:
            self.hosts_list = self._list_hosts()
        return self.hosts_list

    @property
    def vulns(self):
        if not self.vulns_list or not self._completed:
            self.vulns_list = self._list_vulns()
        return self.vulns_list

    def _list_hosts(self):
        """
        Return a list of hosts included in a specified report uuid. 
        """
        raw_list = self.nessus.request_list('report2/hosts', 'hostList', 'host', report=self.uuid)

        hosts = []
        for host in raw_list:
            h = Host(nessus=self.nessus, report=self, hostname=host['hostname'])
            h.total = host['severity']
            level_counts = host['severityCount']['item']
            h.counts = ( level_counts[0], level_counts[1], level_counts[2],
                         level_counts[3], level_counts[4] )

            hosts.append(h)
        
        return hosts

    def _list_vulns(self):
        """
        Return a list of vulnerabilities included in a specified report
        """
        raw_list = self.nessus.request_list('report2/vulnerabilities', 'vulnList', 'vulnerability', report=self.uuid)
        
        vulns = []
        for vuln in raw_list:
            v = Vulnerability(nessus=self.nessus, plugin_id=vuln['plugin_id'], severity=vuln['severity'])
            v._name = vuln['plugin_name'] # unsafe, should use proper setters
            v._family = vuln['plugin_family']
            vulns.append(v)

        return vulns
    
    def hosts_affected_by(self, vuln):
        raw_list = self.nessus.request_list('report2/hosts/plugin', 'hostList', 'host', report=self.uuid, severity=vuln.severity, plugin_id=vuln.plugin_id)

        hosts = []
        for host in raw_list:
            h = Host(nessus=self.nessus, report=self, hostname=host['hostname'])
            hosts.append(h)

        return hosts

    def __str__(self):
        timestamp = time.strftime(
            "%Y-%m-%d %H:%M:%S",
            time.localtime(self.timestamp))
        return """Report "{0}" {1} ({2})""".format(
               self.name, timestamp, self.status)
    def __repr__(self):
        return """Report({0}, {1}, {2}, {3})""".format(
               self.timestamp, self.status, self.uuid, self.name)

@multiton
class Host(object):
    def __init__(self, nessus, report, hostname): #, total, level_counts):
        self.nessus = nessus
        self.report = report
        self.hostname = hostname

        self.total = None
        self.counts = None

    @property
    def info(self):
        return self.counts[0]

    @property
    def low(self):
        return self.counts[1]

    @property
    def med(self):
        return self.counts[2]

    @property
    def high(self):
        return self.counts[3]

    @property
    def critical(self):
        return self.counts[4]

    @property
    def cpe(self):
        try:
            raw_data = self.nessus.request_single('report2/details/plugin', 'portDetails', 'ReportItem', 'data', 'plugin_output', report=self.report.uuid, hostname=self.hostname, port=0, protocol='tcp', severity=0, plugin_id=45590)
        except TypeError: # when cpe doesn't exist for host
            raw_data = ''
        return raw_data

    #def __str__(self):
    #    return "Host {0}".format(self.hostname)

    #def __repr__(self):
    #    return "Host {0} [{1},{2},{3},{4},{5}]".format(self.hostname, self.info, self.low, self.med, self.high, self.critical)

