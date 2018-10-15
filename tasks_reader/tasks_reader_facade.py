from tasks_reader.excel_task_reader import ExcelTaskReader


def read_from_excel(file, sheet, first_row, columns_mapping, last_row, rows_to_skip=None):
    reader = ExcelTaskReader(file, sheet, first_row, columns_mapping, last_row, rows_to_skip=rows_to_skip)
    return reader.read()
