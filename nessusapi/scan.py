# coding=utf-8

class Scan(object):
    def __init__(self, nessus, target, scan_name, policy):
        self.nessus = nessus
        self.target = target
        self.name = scan_name
        self.policy = policy

        self.uuid = self.nessus.request_single('scan/new', 'scan', 'uuid',
                                    target=self.target,
                                    scan_name=self.name,
                                    policy_id=self.policy)

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
        return self.nessus.request_single('scan/{0}'.format(status),
                                          'scan', 'status',
                                          scan_uuid=self.uuid)

class BadRequestError(Exception):
    pass
