# scan.py

class Scan:
    def __init__(self, target, scan_name, policy, session):
        self.target = target
        self.name = scan_name
        self.policy = policy
        self.session = session
        self.uuid = session.request('scan/new', target=self.target,
                                    scan_name=self.name,
                                    policy_id=self.policy)['uuid']
        
    def stop(self):
        return self.changeStatus('stop')

    def pause(self):
        return self.changeStatus('pause')

    def resume(self):
        return self.changeStatus('resume')
    
    def changeStatus(self, status):
        return self.session.request('scan/{0}'.format(status),
                                    scan_uuid=uuid)['status'] == 'OK'
                                    
