class TaskRow:
    def __init__(self, uid, name=None, blockers=None, normal_estimate=None, min_estimate=None, max_estimate=None):
        self.uid = uid
        self.name = name
        self.blockers = blockers
        self.min_estimate = min_estimate
        self.normal_estimate = normal_estimate
        self.max_estimate = max_estimate
