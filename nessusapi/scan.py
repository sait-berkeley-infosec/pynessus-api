from nessusapi.session import request, HTTPError 

class Scan:
    def __init__(self, target, scan_name, policy):
        self.target = target
        self.name = scan_name
        self.policy = policy
        self.uuid = None

    def start(self):
        if self.uuid:
            raise BadRequestError('Scan already started')
        try:
            self.uuid = request('scan/new', target=self.target,
                                        scan_name=self.name,
                                        policy_id=self.policy)['scan']['uuid']
        except HTTPError as e:
            if e.code == 404 and 'Unknown policy' in e.read():
                raise BadRequestError('Unknown policy')
            raise
        
    def stop(self):
        if self.changeStatus('stop') == 'stopping':
            self.uuid = None
            return True
        return False

    def pause(self):
        return self.changeStatus('pause') == 'pausing'

    def resume(self):
        return self.changeStatus('resume') == 'resuming'
    
    def changeStatus(self, status):
        if not self.uuid:
            raise BadRequestError('Scan not started')
        return request('scan/{0}'.format(status),
                       scan_uuid=self.uuid)['scan']['status']
