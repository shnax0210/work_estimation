def filter_task_rows(tasks, predicates):
    result_tasks = []

    for task in tasks:
        errors = _test_task(task, predicates)
        if len(errors) > 0:
            print("Task with uid: '{}' was filtered due to: {}".format(task.uid, errors))
        else:
            result_tasks.append(task)

    return result_tasks


def _test_task(task, predicates):
    return [predicate.message for predicate in predicates if not predicate.test(task)]


class MinEstimateRequiredPredicate:
    @staticmethod
    def test(task):
        return task.min_estimate == 0 or task.min_estimate

    @property
    def message(self):
        return "min_estimate field is required"


class NormalEstimateRequiredPredicate:
    @staticmethod
    def test(task):
        return task.normal_estimate == 0 or task.normal_estimate

    @property
    def message(self):
        return "normal_estimate field is required"


class MaxEstimateRequiredPredicate:
    @staticmethod
    def test(task):
        return task.max_estimate == 0 or task.max_estimate

    @property
    def message(self):
        return "max_estimate field is required"
