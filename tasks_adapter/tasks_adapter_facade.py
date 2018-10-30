from tasks_adapter.blockers_adapter import adapt_blockers, validate_blockers
from work_emulator.task import Task


def adapt_use_normal_estimate(task_rows):
    valid_task_rows, errors = validate_blockers(task_rows)

    tasks = [Task(task_row.uid, task_row.normal_estimate) for task_row in valid_task_rows]
    adapt_blockers(valid_task_rows, tasks)

    return tasks, errors
