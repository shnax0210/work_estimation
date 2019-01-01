import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import work_estimation_facade
from calculator.three_points import ThreePoints
from tasks_adapter import tasks_adapter_facade
from work_emulator import work_emulator_facade


def read_from_excel(file, sheet, first_row, last_row, columns_mapping, rows_to_skip=None, filter_predicates=[]):
    valid_task_rows, task_row_errors = work_estimation_facade.read_from_excel(file=file,
                                                                              sheet=sheet,
                                                                              first_row=first_row,
                                                                              last_row=last_row,
                                                                              columns_mapping=columns_mapping,
                                                                              rows_to_skip=rows_to_skip,
                                                                              filter_predicates=filter_predicates)

    print('Read valid {} task rows'.format(len(valid_task_rows)))
    print('--------------------------------------------')
    for error in task_row_errors:
        print(error)

    return valid_task_rows


def print_normal_distribution_for_task(task_row):
    normal_distribution = work_estimation_facade.calculate_normal_distribution_by_three_points(_convert_task(task_row))
    _print_normal_distribution(normal_distribution, _build_title(task_row))


def print_normal_distribution_for_tasks(task_rows):
    normal_distribution = work_estimation_facade.calculate_sum_normal_distribution_by_three_points(
        _convert_tasks(task_rows))
    _print_normal_distribution(normal_distribution, 'Total')


def emulate_use_normal_estimate(task_rows, number_of_workers):
    valid_tasks, task_errors = tasks_adapter_facade.adapt_use_normal_estimate(task_rows)
    _print_validation_results(task_rows, valid_tasks, task_errors)

    history_records = work_emulator_facade.emulate(number_of_workers, valid_tasks)

    history_data = dict()
    history_data['day'] = [history_record.day for history_record in history_records]

    for cell_index in range(len(history_records[0].cells)):
        worker_name = history_records[0].cells[cell_index].worker_name
        history_data[worker_name] = [record.cells[cell_index].task_uid for record in history_records]

    history_data_frame = pd.DataFrame(data=history_data)
    history_data_frame.set_index('day', inplace=True)
    print(history_data_frame)


def emulate_use_monte_carlo_method(task_rows, number_of_workers, number_of_emulation):
    valid_task, task_errors = tasks_adapter_facade.adapt_use_probability_estimate(task_rows)
    _print_validation_results(task_rows, valid_task, task_errors)

    def _emulate():
        valid_tasks, task_errors = tasks_adapter_facade.adapt_use_probability_estimate(task_rows)
        return work_emulator_facade.emulate(number_of_workers, valid_tasks)

    required_days_for_emulations = [len(_emulate()) for emulation_index in range(number_of_emulation)]
    normal_distribution = work_estimation_facade.calculate_normal_distribution_by_x(required_days_for_emulations)

    _print_normal_distribution(normal_distribution, 'Monte Carlo emulation')


def _print_normal_distribution(normal_distribution, title):
    def find_cell_size(min_x, max_x):
        max_number_of_cells = 15

        if (max_x - min_x) > max_number_of_cells:
            return (max_x - min_x) // max_number_of_cells

        return 1

    fig = plt.figure()
    ax = fig.gca()
    ax.set_xticks(np.arange(normal_distribution.min_x, normal_distribution.max_x,
                            find_cell_size(normal_distribution.min_x, normal_distribution.max_x)))
    ax.set_yticks(np.arange(0, 1.1, 0.1))
    fig.suptitle(title, fontsize=14)
    plt.xlabel('Estimate', fontsize=14)
    plt.ylabel('Probability', fontsize=14)

    plt.plot(normal_distribution.x, normal_distribution.y)
    plt.grid()
    plt.show()


def _build_title(task):
    if task.name:
        return "{}:{}".format(task.uid, task.name)
    else:
        return task.uid


def _convert_task(task_row):
    return ThreePoints(task_row.min_estimate, task_row.normal_estimate, task_row.max_estimate)


def _convert_tasks(task_rows):
    return [_convert_task(task_row) for task_row in task_rows]


def _print_validation_results(all_tasks, valid_tasks, task_errors):
    print('----------------------------------------------------------------------------------------')
    print('{} task rows are valid for emulation from {}'.format(len(valid_tasks), len(all_tasks)))
    print('----------------------------------------------------------------------------------------')
    if len(task_errors) > 0:
        print('Next errors occurred:')
        for error in task_errors:
            print(error)
        print('----------------------------------------------------------------------------------------')
