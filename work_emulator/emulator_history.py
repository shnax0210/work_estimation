class EmulationHistoryCell:
    def __init__(self, worker_name, task_uid):
        self.worker_name = worker_name
        self.task_uid = task_uid


class EmulationHistoryRow:
    def __init__(self, day):
        self.day = day
        self.cells = []

    def add_cell(self, cell):
        self.cells.append(cell)


class EmulationHistory:
    def __init__(self):
        self.records = dict()

    def record(self, day, worker_name, task_uid):
        if day not in self.records:
            self.records[day] = EmulationHistoryRow(day)

        self.records[day].add_cell(EmulationHistoryCell(worker_name, task_uid))

    def get_recorded(self):
        return sorted(self.records.values(), key=lambda row: row.day)
