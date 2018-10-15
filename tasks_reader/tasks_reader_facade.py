from tasks_reader.excel_task_reader import ExcelTaskReader


def read_from_excel(file, sheet, first_row, columns_mapping, last_row):
    reader = ExcelTaskReader(file, sheet, first_row, columns_mapping, last_row)
    return reader.read()
