class BlockedEffortTaskPrioritizeStrategy:
    def get_most_prioritized(self, tasks):
        return self._find_most_prioritized_by_blocked_effort(tasks) or self._find_most_prioritized_by_required_effort(
            tasks)

    def _create_blocked_effort_to_task_mapping(self, tasks):
        return dict([(self._calculate_blocked_effort(task), task) for task in tasks])

    def _calculate_blocked_effort(self, task):
        blocked_effort = 0

        for task_blocked_by in task.tasks_blocked_by:
            blocked_effort += task_blocked_by.required_effort + self._calculate_blocked_effort(task_blocked_by)

        return blocked_effort

    def _find_most_prioritized_by_blocked_effort(self, tasks):
        blocked_effort_to_task = self._create_blocked_effort_to_task_mapping(tasks)
        max_blocked_effort = max([effort for (effort, task) in blocked_effort_to_task.items()])

        if max_blocked_effort != 0:
            return blocked_effort_to_task.get(max_blocked_effort)
        else:
            return None

    @staticmethod
    def _find_most_prioritized_by_required_effort(tasks):
        required_effort_to_task = dict([(task.required_effort, task) for task in tasks])
        min_required_effort = min([effort for (effort, task) in required_effort_to_task.items()])

        return required_effort_to_task.get(min_required_effort)
