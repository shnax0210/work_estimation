from work_emulator.emulator_history import EmulationHistory


class Emulator:
    def __init__(self, workers, task_board):
        self.workers = workers
        self.task_board = task_board
        self.history = EmulationHistory()

    def emulate(self):
        day = 1
        while not self.task_board.are_all_tasks_completed():
            self._assign_open_tasks_to_free_workers()
            self._emulate_one_day(day)
            day += 1

        return self.history.get_recorded()

    def get_history(self):
        return self.history

    def _get_free_workers(self):
        return [worker for worker in self.workers if worker.is_free()]

    def _assign_open_tasks_to_free_workers(self):
        for worker in self._get_free_workers():
            if not self.task_board.has_open_tasks():
                return
            worker.assign(self.task_board.get_most_prioritized_open_task())

    def _emulate_one_day(self, day):
        for worker in self.workers:
            self._record_history(worker, day)
            worker.work_one_day()

    def _record_history(self, worker, day):
        self.history.record(day, worker.name, worker.task_uid)
