from work_emulator.emulator import Emulator
from work_emulator.task_board import TaskBoard
from work_emulator.task_prioritize_strategies import BlockedEffortTaskPrioritizeStrategy
from work_emulator.task_validators import TasksValidatorComposite, TasksUniqueNamesValidator, \
    TasksDependencyLoopsValidator
from work_emulator.worker import Worker


class WorkEmulatorFacade:
    def __init__(self, number_of_workers, task_provider):
        self.number_of_workers = number_of_workers
        self.task_provider = task_provider

    def emulate(self):
        emulator = Emulator(self.create_workers(), self.create_task_board())
        return emulator.emulate()

    def create_workers(self):
        return [Worker("worker{}".format(index)) for index in range(self.number_of_workers)]

    def create_task_board(self):
        task_board = TaskBoard(BlockedEffortTaskPrioritizeStrategy(),
                               TasksValidatorComposite([TasksUniqueNamesValidator(), TasksDependencyLoopsValidator()]))
        task_board.add_tasks(self.task_provider.get_all())
        return task_board
