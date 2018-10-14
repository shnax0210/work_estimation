from work_emulator.task import TaskStatus


class Worker:
    def __init__(self, name):
        self.name = name
        self.task = None

    def assign(self, task):
        self.task = task
        task.assign(self)

    def is_free(self):
        return self.task is None

    def work_one_day(self):
        if self.is_free():
            return

        self.task.do_effort(1)

        if self.task.get_status() == TaskStatus.COMPLETED:
            self.task = None

    def get_task_name(self):
        if self.task is not None:
            return self.task.get_name()

        return None

    def get_name(self):
        return self.name
