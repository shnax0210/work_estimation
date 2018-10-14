from enum import Enum


class TaskStatus(Enum):
    OPEN = 0
    BLOCKED = 1
    IN_PROGRESS = 2
    COMPLETED = 3


class Task:
    def __init__(self, uid, required_effort):
        self.uid = uid
        self.required_effort = required_effort
        self.left_effort = required_effort
        self.blockers = set()
        self.tasks_blocked_by = set()
        self.worker = None

    def assign(self, worker):
        self.worker = worker

    def do_effort(self, effort_amount):
        if effort_amount > self.left_effort:
            raise ValueError('Left effort is less that new effort that has been done')

        self.left_effort -= effort_amount

    @property
    def status(self):
        if self.left_effort == 0:
            return TaskStatus.COMPLETED

        if self._has_not_completed_blockers():
            return TaskStatus.BLOCKED

        if self.worker is not None:
            return TaskStatus.IN_PROGRESS

        return TaskStatus.OPEN

    def add_blocker(self, blocker):
        self.blockers.add(blocker)
        blocker.add_task_blocked_by(self)

    def add_task_blocked_by(self, task_blocked_by):
        self.tasks_blocked_by.add(task_blocked_by)

    def _has_not_completed_blockers(self):
        return len([blocker for blocker in self.blockers if blocker.status != TaskStatus.COMPLETED]) > 0
