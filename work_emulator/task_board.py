from work_emulator.emulator_exception import WorkEmulatorException
from work_emulator.task import TaskStatus


class TaskBoard:
    def __init__(self, task_prioritize_strategy, tasks_validator):
        self.tasks = []
        self.task_prioritize_strategy = task_prioritize_strategy
        self.tasks_validator = tasks_validator

    def are_all_tasks_completed(self):
        return all(task.get_status() == TaskStatus.COMPLETED for task in self.tasks)

    def has_open_tasks(self):
        return len(self._get_open_tasks()) > 0

    def get_most_prioritized_open_task(self):
        return self.task_prioritize_strategy.get_most_prioritized(self._get_open_tasks())

    def add_tasks(self, new_tasks):
        error = self.tasks_validator.validate(self.tasks + new_tasks)
        if error is not None:
            raise WorkEmulatorException(self._create_message_for_error_during_add(error))

        self.tasks.extend(new_tasks)

    @staticmethod
    def _create_message_for_error_during_add(error):
        return 'Next error found during tasks adding: {}'.format(error)

    def _get_open_tasks(self):
        return [task for task in self.tasks if task.get_status() == TaskStatus.OPEN]
