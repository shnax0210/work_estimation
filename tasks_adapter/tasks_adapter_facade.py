from calculator.calculator_facade import calculate_task_mean_and_std
from tasks_adapter.blockers_adapter import adapt_blockers, validate_blockers
from work_emulator.task import Task
import scipy.stats as stats


def _adapt(task_rows, estimate_function):
    valid_task_rows, errors = validate_blockers(task_rows)

    tasks = [Task(task_row.uid, estimate_function(task_row)) for task_row in valid_task_rows]
    adapt_blockers(valid_task_rows, tasks)

    return tasks, errors


def adapt_use_normal_estimate(task_rows):
    return _adapt(task_rows, lambda task_row: task_row.normal_estimate)


def adapt_use_probability_estimate(task_rows):
    def generate_probability_estimate(task_row):
        mean, std = calculate_task_mean_and_std(task_row)
        return max(0., round(stats.norm.rvs(mean, std, size=1)[0]))

    return _adapt(task_rows, generate_probability_estimate)
