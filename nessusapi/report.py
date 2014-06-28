from nessusapi.session import request

def list_reports():
    """
    Return a list of available reports from the Nessus server.

    Each report is an OrderedDict with the following useful fields:
    timestamp -- the time the scan was created, as POSIX time
    status -- the status of the report, e.g. 'completed'
    name -- the uuid of the report
    readableName -- the human-readable name specified for the report
    """
    return _ensure_list(request('report/list')['reports']['report'])

def list_hosts(report):
    """
    Return a list of hosts included in a specified report uuid. 

    Each host is an OrderedDict with many fields, but the most useful
    one is:
    hostname -- the hostname of the host (e.g. server1.domain.org)
    """
    return _ensure_list(request('report/hosts', report=report)['hostList']['host'])

def list_vulns(report):
    """
    Return a list of vulnerabilities included in a specified report uuid.

    Each vuln is an OrderedDict with the following useful fields:
    plugin_id -- numeric ID by which Nessus identifies the plugin 
    plugin_name -- the human-readable name for the plugin
    plugin_family -- the family which the plugin is in, e.g. 'DNS'
    count -- the number of occurrences of the vulnerability in the report
    severity -- the severity from 0 to 5, 0 being the least severe
    """
    return _ensure_list(request('report2/vulnerabilities', report=report)['vulnList']['vulnerability'])

def list_affected_hosts(report, plugin, severity):
    """
    Return a list of hosts affected by a specified plugin.

    For some reason, Nessus requires that the severity also be included.
    Each host is an OrderedDict with the following useful fields:
    hostname -- the hostname of the host (e.g. server1.domain.org)
    port -- the port to which the plugin applies
    protocol -- the protocol (typically tcp or udp) to which the plugin applies
    """
    return _ensure_list(request('report2/hosts/plugin', report=report, plugin_id=plugin, severity=severity)['hostList']['host'])

# requests sometimes do not return lists, so make them lists
def _ensure_list(obj):
    if not isinstance(obj, list):
        return [obj]
    return obj
