# report.py

from session import request

def list_reports():
    return ensure_list(request('report/list')['reports']['report'])

def list_hosts(report):
    return ensure_list(request('report/hosts', report=report)['hostList']['host'])

def list_vulns(report):
    return ensure_list(request('report2/vulnerabilities', report=report)['vulnList']['vulnerability'])

def list_affected_hosts(report, plugin, severity):
    return ensure_list(request('report2/hosts/plugin', report=report, plugin_id=plugin, severity=severity)['hostList']['host'])

# above requests return non-lists for single items
def ensure_list(obj):
    if type(obj) != type([]):
        return [ obj ]
    return obj
