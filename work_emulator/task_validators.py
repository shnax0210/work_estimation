from collections import OrderedDict
from itertools import groupby


class TasksValidatorComposite:
    def __init__(self, validators):
        self.validators = validators

    def validate(self, tasks):
        sorted_tasks = sorted(tasks, key=lambda task: task.get_name())
        for validator in self.validators:
            error = validator.validate(sorted_tasks)
            if error is not None:
                return error
        return None


class TasksUniqueNamesValidator:
    def validate(self, tasks):
        not_unique_names = self._find_not_unique_names(tasks)
        if len(not_unique_names) > 0:
            return "There are tasks that have duplicated names: " + str(not_unique_names)

        return None

    @staticmethod
    def _find_not_unique_names(tasks):
        name_to_tasks = groupby(tasks, lambda task: task.get_name())
        return [name for name, tasks_with_name in name_to_tasks if len(list(tasks_with_name)) > 1]


class TasksDependencyLoopsValidator:
    def validate(self, tasks):
        dependency_loops = self._find_dependency_loops(tasks)
        if len(dependency_loops) > 0:
            return "There are next dependency loops: " + str(dependency_loops)

        return None

    def _find_dependency_loops(self, tasks):
        dependency_loops = []

        for task in tasks:
            dependency_loops.extend(self._find_dependency_loops_for_task(task, []))

        return self._filter_duplicated_loops(dependency_loops)

    def _find_dependency_loops_for_task(self, task, dependency_chain):
        if task.get_name() in dependency_chain:
            dependency_chain.append(task.get_name())
            return [dependency_chain]

        dependency_chain.append(task.get_name())
        dependency_loops = []

        for blocker in task.get_blockers():
            dependency_loops.extend(self._find_dependency_loops_for_task(blocker, dependency_chain.copy()))

        return dependency_loops

    @staticmethod
    def _filter_duplicated_loops(dependency_loops):
        unique_dependency_loops = OrderedDict()

        for loop in dependency_loops:
            if loop[0] != loop[-1]:
                continue

            loop_key = tuple(sorted(loop[:-1]))
            if loop_key not in unique_dependency_loops:
                unique_dependency_loops[loop_key] = loop

        return [loop for loop_key, loop in unique_dependency_loops.items()]
