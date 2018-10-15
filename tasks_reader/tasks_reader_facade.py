from tasks_reader.excel_task_reader import ExcelTaskReader


def read_from_excel(file, sheet, first_row, last_row, columns_mapping, rows_to_skip=None):
    reader = ExcelTaskReader(file, sheet, first_row, last_row, columns_mapping, rows_to_skip=rows_to_skip)
    return reader.read()
