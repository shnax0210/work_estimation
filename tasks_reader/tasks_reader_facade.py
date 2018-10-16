from tasks_reader.excel_task_reader import ExcelTaskReader
from tasks_reader.tasks_filter import filter_tasks


def read_from_excel(file, sheet, first_row, last_row, columns_mapping, rows_to_skip=None, filter_predicates=[]):
    reader = ExcelTaskReader(file, sheet, first_row, last_row, columns_mapping, rows_to_skip=rows_to_skip)
    all_tasks = reader.read()

    return filter_tasks(all_tasks, filter_predicates)
