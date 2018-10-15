import unittest

from tasks_reader.tasks_reader_facade import read_from_excel


class TaskReaderFacadeTest(unittest.TestCase):
    def test_read_from_excel(self):
        # Given
        file = "test_resources/test_tasks.xlsx"
        sheet = "tasks"
        first_row = 4
        last_row = 9
        columns_mapping = {
            'uid': 'A',
            'name': 'B',
            'blockers': 'C',
            'min_estimate': 'E',
            'normal_estimate': 'F',
            'max_estimate': 'G'
        }

        # When
        tasks = read_from_excel(file, sheet, first_row, columns_mapping, last_row)

        #
        self.assertEqual(6, len(tasks))
        self._check_task(tasks[0],
                         uid='TASK-1',
                         name='Base functionality implementations.',
                         blockers=[],
                         min_estimate=3,
                         normal_estimate=5,
                         max_estimate=13)
        self._check_task(tasks[1],
                         uid='TASK-2',
                         name='First page implementation.',
                         blockers=['TASK-1'],
                         min_estimate=1,
                         normal_estimate=3,
                         max_estimate=8)
        self._check_task(tasks[2],
                         uid='TASK-3',
                         name='Popup implementation.',
                         blockers=['TASK-1'],
                         min_estimate=None,
                         normal_estimate=None,
                         max_estimate=None)
        self._check_task(tasks[3],
                         uid='TASK-4',
                         name='Integration tests for first page and popup.',
                         blockers=['TASK-2', 'TASK-3'],
                         min_estimate=5,
                         normal_estimate=13,
                         max_estimate=20)
        self._check_task(tasks[4],
                         uid='TASK-5',
                         name='Cart calculation logic - Part 1',
                         blockers=[],
                         min_estimate=13,
                         normal_estimate=20,
                         max_estimate=40)
        self._check_task(tasks[5],
                         uid='TASK-6',
                         name='Second page implementation.',
                         blockers=['TASK-2'],
                         min_estimate=None,
                         normal_estimate=40,
                         max_estimate=None)

    def _check_task(self, task, uid, name, blockers, min_estimate, normal_estimate, max_estimate):
        self.assertEqual(uid, task.uid)
        self.assertEqual(name, task.name)
        self.assertEqual(blockers, task.blockers)
        self.assertEqual(min_estimate, task.min_estimate)
        self.assertEqual(normal_estimate, task.normal_estimate)
        self.assertEqual(max_estimate, task.max_estimate)
