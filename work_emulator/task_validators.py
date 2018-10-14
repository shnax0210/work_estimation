from collections import OrderedDict
from itertools import groupby


class TasksValidatorComposite:
    def __init__(self, validators):
        self.validators = validators

    def validate(self, tasks):
        sorted_tasks = sorted(tasks, key=lambda task: task.uid)
        for validator in self.validators:
            error = validator.validate(sorted_tasks)
            if error is not None:
                return error
        return None


class TasksUniqueUidsValidator:
    def validate(self, tasks):
        not_unique_uids = self._find_not_unique_uids(tasks)
        if len(not_unique_uids) > 0:
            return "There are tasks that have duplicated uids: " + str(not_unique_uids)

        return None

    @staticmethod
    def _find_not_unique_uids(tasks):
        uid_to_tasks = groupby(tasks, lambda task: task.uid)
        return [uid for uid, tasks_with_uid in uid_to_tasks if len(list(tasks_with_uid)) > 1]


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
        if task.uid in dependency_chain:
            dependency_chain.append(task.uid)
            return [dependency_chain]

        dependency_chain.append(task.uid)
        dependency_loops = []

        for blocker in task.blockers:
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
