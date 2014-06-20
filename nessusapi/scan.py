# scan.py

from session import require_auth

class Scan:
    def __init__(self, target, scan_name, policy):
        self.target = target
        self.name = scan_name
        self.policy = policy

    @require_auth
    def start(self):
        self.uuid = self.session.request('scan/new', target=self.target,
                                    scan_name=self.name,
                                    policy_id=self.policy)['scan']['uuid']
        
    def stop(self):
        return self.changeStatus('stop')

    def pause(self):
        return self.changeStatus('pause')

    def resume(self):
        return self.changeStatus('resume')
    
    @require_auth
    def changeStatus(self, status):
        return self.session.request('scan/{0}'.format(status),
                                    scan_uuid=uuid)['status'] == 'OK'
                                    
