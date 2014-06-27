# report.py

from session import request

def list_reports():
    """
    Return a list of available reports from the Nessus server.
    Each report is an OrderedDict with the following useful fields:
        - timestamp : The time the scan was originally created, formatted as POSIX time.
        - status : The status of the report, e.g. 'completed'.
        - name : The uuid of the report.
        - readableName : The human-readable name specified for the report.
    """
    return ensure_list(request('report/list')['reports']['report'])

def list_hosts(report):
    """
    Return a list of hosts included in a specified report uuid. 
    Each item is an OrderedDict with many fields, but the only useful
    one is:
        - hostname : The hostname of the host (e.g. server1.domain.org)
    """
    return ensure_list(request('report/hosts', report=report)['hostList']['host'])

def list_vulns(report):
    """
    Return a list of vulnerabilities included in a specified report uuid.
    Each item is an OrderedDict with the following useful fields:
        - plugin_id : Numeric ID by which Nessus identifies the plugin.
        - plugin_name : The human-readable name for the plugin.
        - plugin_family : The family which the plugin is in, e.g. 'DNS'.
        - count : The number of occurrences of the vulnerability are present
        in the report.
        - severity : The severity of the vulnerability from 0 to 5, 0 being
        the least severe (often just information) and 5 being most severe (e.g.
        a remote code execution vulnerability.)
    """
    return ensure_list(request('report2/vulnerabilities', report=report)['vulnList']['vulnerability'])

def list_affected_hosts(report, plugin, severity):
    """
    Return a list of hosts affected by a specified plugin.
    For some reason, Nessus requires that the severity also be included.
    Each item is an OrderedDict with the following useful fields for each host:
        - hostname : The hostname of the host (e.g. server1.domain.org)
        - port : The port to which the plugin applies
        - protocol : The protocol (typically tcp or udp) to which the plugin
        applies
    """
    return ensure_list(request('report2/hosts/plugin', report=report, plugin_id=plugin, severity=severity)['hostList']['host'])

# above requests return non-lists for single items, this makes them all lists
def ensure_list(obj):
    if type(obj) != type([]):
        return [ obj ]
    return obj
