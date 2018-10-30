from work_emulator.emulator import Emulator
from work_emulator.task_board import TaskBoard
from work_emulator.task_prioritize_strategies import BlockedEffortTaskPrioritizeStrategy
from work_emulator.task_validators import TasksValidatorComposite, TasksUniqueUidsValidator, \
    TasksDependencyLoopsValidator
from work_emulator.worker import Worker


def emulate(number_of_workers, tasks):
    emulator = Emulator(_create_workers(number_of_workers), _create_task_board(tasks))
    return emulator.emulate()


def _create_workers(number_of_workers):
    return [Worker("worker{}".format(index)) for index in range(number_of_workers)]


def _create_task_board(tasks):
    task_board = TaskBoard(BlockedEffortTaskPrioritizeStrategy(),
                           TasksValidatorComposite([TasksUniqueUidsValidator(), TasksDependencyLoopsValidator()]))
    task_board.add_tasks(tasks)
    return task_board
