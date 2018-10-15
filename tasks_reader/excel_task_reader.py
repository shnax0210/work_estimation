import openpyxl

from tasks_reader.raw_task import RawTask


class ExcelTaskReader:
    def __init__(self, file, sheet, first_row, columns_mapping, last_row, array_delimiter=','):
        self.file = file
        self.sheet = sheet
        self.first_row = first_row
        self.columns_mapping = columns_mapping
        self.last_row = last_row
        self.array_delimiter = array_delimiter

    def read(self):
        wb = openpyxl.load_workbook(filename=self.file)
        sheet = wb[self.sheet]

        return [self._create_task(sheet, row_index) for row_index in range(self.first_row, self.last_row + 1)]

    def _create_task(self, sheet, row_index):
        return RawTask(uid=self._fetch_string(sheet, row_index, 'uid'),
                       name=self._fetch_string(sheet, row_index, 'name'),
                       blockers=self._fetch_array(sheet, row_index, 'blockers'),
                       min_estimate=self._fetch_int(sheet, row_index, 'min_estimate'),
                       normal_estimate=self._fetch_int(sheet, row_index, 'normal_estimate'),
                       max_estimate=self._fetch_int(sheet, row_index, 'max_estimate'))

    def _fetch_array(self, sheet, row_index, column_name):
        string_value = self._fetch_string(sheet, row_index, column_name)
        if not string_value:
            return []

        return string_value.split(self.array_delimiter)

    def _fetch_int(self, sheet, row_index, column_name):
        string_value = self._fetch_string(sheet, row_index, column_name)
        if not string_value:
            return None

        return int(float(string_value))

    def _fetch_string(self, sheet, row_index, column_name):
        cell_value = self._fetch_cell_value(sheet, row_index, column_name)
        if not cell_value:
            return ''

        return str(cell_value).strip()

    def _fetch_cell_value(self, sheet, row_index, column_name):
        column = self.columns_mapping[column_name]
        return sheet['{}{}'.format(column, row_index)].value
