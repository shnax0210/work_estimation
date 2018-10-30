import unittest

from tasks_adapter.tasks_adapter_facade import adapt_use_normal_estimate
from tasks_reader.task_row import TaskRow

TASK_UID1 = 'task1'
TASK_UID2 = 'task2'
TASK_UID3 = 'task3'
TASK_UID4 = 'task4'
TASK_UID5 = 'task5'
TASK_UID6 = 'task6'
TASK_UID7 = 'task7'
NOT_EXISTED_TASK_UID = 'task8'


class TasksAdapterTest(unittest.TestCase):
    def test_adaptation_of_tasks_with_normal_estimate(self):
        # Given
        task_rows = [TaskRow(uid=TASK_UID1, normal_estimate=5, blockers=[]),
                     TaskRow(uid=TASK_UID2, normal_estimate=3, blockers=[TASK_UID1]),
                     TaskRow(uid=TASK_UID3, normal_estimate=13, blockers=[NOT_EXISTED_TASK_UID]),
                     TaskRow(uid=TASK_UID4, normal_estimate=8, blockers=[TASK_UID1, TASK_UID3]),
                     TaskRow(uid=TASK_UID5, normal_estimate=2, blockers=[TASK_UID1]),
                     TaskRow(uid=TASK_UID6, normal_estimate=13, blockers=[TASK_UID2, TASK_UID4]),
                     TaskRow(uid=TASK_UID7, normal_estimate=13, blockers=[TASK_UID2, TASK_UID5])]

        # When
        tasks, errors = adapt_use_normal_estimate(task_rows)

        # Then
        self.assertEqual(4, len(tasks))
        self._check_task(tasks[0], TASK_UID1, 5, [])
        self._check_task(tasks[1], TASK_UID2, 3, [TASK_UID1])
        self._check_task(tasks[2], TASK_UID5, 2, [TASK_UID1])
        self._check_task(tasks[3], TASK_UID7, 13, [TASK_UID2, TASK_UID5])

        self.assertEqual(3, len(errors))
        self.assertEqual("Task task3 filtered due to missing of last blocker in chain: ['task8']", errors[0])
        self.assertEqual("Task task4 filtered due to missing of last blocker in chain: ['task3', 'task8']", errors[1])
        self.assertEqual("Task task6 filtered due to missing of last blocker in chain: ['task4', 'task3', 'task8']",
                         errors[2])

    def _check_task(self, task, uid, required_effort, blockers):
        self.assertEqual(uid, task.uid)
        self.assertEqual(required_effort, task.required_effort)
        self.assertEqual(set(blockers), set([blocker.uid for blocker in task.blockers]))
