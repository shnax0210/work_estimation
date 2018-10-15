import openpyxl

from tasks_reader.raw_task import RawTask

ROWS_TO_SKIP_RANGE_DELIMITER = ':'
ROWS_TO_SKIP_DELIMITER = ','


class ExcelTaskReader:
    def __init__(self, file, sheet, first_row, columns_mapping, last_row, array_delimiter=',', rows_to_skip=None):
        self.file = file
        self.sheet = sheet
        self.first_row = first_row
        self.columns_mapping = columns_mapping
        self.last_row = last_row
        self.array_delimiter = array_delimiter
        self.rows_to_skip = rows_to_skip

    def read(self):
        wb = openpyxl.load_workbook(filename=self.file)
        sheet = wb[self.sheet]
        parsed_rows_to_skip = self._parse_rows_to_skip()

        return [self._create_task(sheet, row_index) for row_index in range(self.first_row, self.last_row + 1) if
                row_index not in parsed_rows_to_skip]

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

    def _parse_rows_to_skip(self):
        result = set()

        if self.rows_to_skip is None:
            return result

        for row_or_range in self.rows_to_skip.split(ROWS_TO_SKIP_DELIMITER):
            if ROWS_TO_SKIP_RANGE_DELIMITER in row_or_range:
                result.update(self._parse_rows_to_skip_range(row_or_range))
            else:
                result.add(int(float(row_or_range)))

        return result

    @staticmethod
    def _parse_rows_to_skip_range(row_range):
        row_range_parts = row_range.split(ROWS_TO_SKIP_RANGE_DELIMITER)
        first_row = int(float(row_range_parts[0]))
        last_row = int(float(row_range_parts[1]))

        return set([row_index for row_index in range(first_row, last_row + 1)])
