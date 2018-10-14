import unittest

from work_emulator.emulator_exception import WorkEmulatorException
from work_emulator.task import Task
from work_emulator.work_emulator_facade import WorkEmulatorFacade

TASK_UID1 = 'task1'
TASK_UID2 = 'task2'
TASK_UID3 = 'task3'
TASK_UID4 = 'task4'
TASK_UID5 = 'task5'
TASK_UID6 = 'task6'


class WorkEmulatorFacadeTest(unittest.TestCase):
    def test_emulation(self):
        # Given
        work_emulator_facade = WorkEmulatorFacade(2, MockTaskProvider(create_valid_tasks()))

        # When
        history = work_emulator_facade.emulate()

        # Then
        self.assertEqual(len(history), 12)

        self.assertSetEqual({TASK_UID4, None}, convert_cells_to_task_set(history[0]))
        self.assertSetEqual({TASK_UID4, None}, convert_cells_to_task_set(history[1]))
        self.assertSetEqual({TASK_UID1, TASK_UID5}, convert_cells_to_task_set(history[2]))
        self.assertSetEqual({TASK_UID1, TASK_UID5}, convert_cells_to_task_set(history[3]))
        self.assertSetEqual({TASK_UID3, TASK_UID6}, convert_cells_to_task_set(history[4]))
        self.assertSetEqual({TASK_UID3, TASK_UID6}, convert_cells_to_task_set(history[5]))
        self.assertSetEqual({TASK_UID3, TASK_UID6}, convert_cells_to_task_set(history[6]))
        self.assertSetEqual({TASK_UID2, TASK_UID6}, convert_cells_to_task_set(history[7]))
        self.assertSetEqual({TASK_UID2, None}, convert_cells_to_task_set(history[8]))
        self.assertSetEqual({TASK_UID2, None}, convert_cells_to_task_set(history[9]))
        self.assertSetEqual({TASK_UID2, None}, convert_cells_to_task_set(history[10]))
        self.assertSetEqual({TASK_UID2, None}, convert_cells_to_task_set(history[11]))

    def test_error_when_tasks_duplicated_names(self):
        # Given
        work_emulator_facade = WorkEmulatorFacade(2, MockTaskProvider(create_tasks_with_duplicated_uids()))

        # When
        try:
            work_emulator_facade.emulate()
            self.fail()
        except WorkEmulatorException as error:
            # Then
            self.assertEqual(
                "Next error found during tasks adding: There are tasks that have duplicated uids: ['task1', 'task5']",
                str(error))

    def test_error_when_tasks_have_dependency_loops(self):
        # Given
        work_emulator_facade = WorkEmulatorFacade(2, MockTaskProvider(create_tasks_with_dependency_loops()))

        # When
        try:
            work_emulator_facade.emulate()
            self.fail()
        except WorkEmulatorException as error:
            # Then
            self.assertEqual(
                "Next error found during tasks adding: "
                "There are next dependency loops: [['task1', 'task3', 'task1'], ['task2', 'task5', 'task4', 'task2']]",
                str(error))


def create_tasks_with_duplicated_uids():
    task1 = Task(TASK_UID1, 2)
    task2 = Task(TASK_UID2, 5)
    task3 = Task(TASK_UID1, 3)
    task4 = Task(TASK_UID4, 2)
    task5 = Task(TASK_UID5, 2)
    task6 = Task(TASK_UID5, 4)

    return [task1, task2, task3, task4, task5, task6]


def create_tasks_with_dependency_loops():
    task1 = Task(TASK_UID1, 2)
    task2 = Task(TASK_UID2, 5)
    task3 = Task(TASK_UID3, 3)
    task4 = Task(TASK_UID4, 2)
    task5 = Task(TASK_UID5, 2)
    task6 = Task(TASK_UID6, 4)

    task1.add_blocker(task3)
    task3.add_blocker(task1)

    task2.add_blocker(task5)
    task5.add_blocker(task4)
    task4.add_blocker(task2)

    task6.add_blocker(task4)

    return [task1, task2, task3, task4, task5, task6]


def create_valid_tasks():
    task1 = Task(TASK_UID1, 2)
    task2 = Task(TASK_UID2, 5)
    task3 = Task(TASK_UID3, 3)
    task4 = Task(TASK_UID4, 2)
    task5 = Task(TASK_UID5, 2)
    task6 = Task(TASK_UID6, 4)

    task2.add_blocker(task5)
    task5.add_blocker(task4)
    task3.add_blocker(task1)
    task1.add_blocker(task4)
    task6.add_blocker(task4)

    return [task1, task2, task3, task4, task5, task6]


def convert_cells_to_task_set(history_row):
    return set([cell.get_task_uid() for cell in history_row.get_cells()])


class MockTaskProvider:
    def __init__(self, tasks):
        self.tasks = tasks

    def get_all(self):
        return self.tasks


if __name__ == '__main__':
    unittest.main()
