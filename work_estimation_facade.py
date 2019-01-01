from calculator import calculator_facade
from tasks_reader import tasks_reader_facade


def read_from_excel(file, sheet, first_row, last_row, columns_mapping, rows_to_skip=None, filter_predicates=[]):
    return tasks_reader_facade.read_from_excel(file=file,
                                               sheet=sheet,
                                               first_row=first_row,
                                               last_row=last_row,
                                               columns_mapping=columns_mapping,
                                               rows_to_skip=rows_to_skip,
                                               filter_predicates=filter_predicates)


def calculate_normal_distribution_by_three_points(three_points, number_of_points=50):
    return calculator_facade.calculate_normal_distribution_by_three_points(three_points, number_of_points)


def calculate_sum_normal_distribution_by_three_points(three_points_array, number_of_points=50):
    return calculator_facade.calculate_sum_normal_distribution_by_three_points(three_points_array, number_of_points)


def calculate_normal_distribution_by_x(x, number_of_points=50):
    return calculator_facade.calculate_normal_distribution_by_x(x, number_of_points)
