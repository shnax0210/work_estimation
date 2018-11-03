import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import math
import pandas as pd

from calculator.calculator_facade import calculate_task_mean_and_std
from tasks_adapter import tasks_adapter_facade
from work_emulator import work_emulator_facade


def _print_normal_distribution(mean, std, title):
    def find_cell_size(min_x, max_x):
        max_number_of_cells = 15

        if (max_x - min_x) > max_number_of_cells:
            return (max_x - min_x) // max_number_of_cells

        return 1

    min_x = int(round((mean - 4 * std)))
    max_x = int(round((mean + 4 * std)))

    x = np.linspace(min_x, max_x, 50)
    y = stats.norm.cdf(x, mean, std)

    fig = plt.figure()
    ax = fig.gca()
    ax.set_xticks(np.arange(min_x, max_x, find_cell_size(min_x, max_x)))
    ax.set_yticks(np.arange(0, 1.1, 0.1))
    fig.suptitle(title, fontsize=14)
    plt.xlabel('Estimate', fontsize=14)
    plt.ylabel('Probability', fontsize=14)

    plt.plot(x, y)
    plt.grid()
    plt.show()


def _build_title(task):
    if task.name:
        return "{}:{}".format(task.uid, task.name)
    else:
        return task.uid


def print_normal_distribution_for_task(task_row):
    mean, std = calculate_task_mean_and_std(task_row)
    _print_normal_distribution(mean, std, _build_title(task_row))


def print_normal_distribution_for_tasks(task_rows):
    total_mean = sum([calculate_task_mean_and_std(task_row)[0] for task_row in task_rows])
    total_std = math.sqrt(sum([calculate_task_mean_and_std(task_row)[1] for task_row in task_rows]))

    _print_normal_distribution(total_mean, total_std, 'Total')


def _print_validation_results(all_tasks, valid_tasks, task_errors):
    print('----------------------------------------------------------------------------------------')
    print('{} task rows are valid for emulation from {}'.format(len(valid_tasks), len(all_tasks)))
    print('----------------------------------------------------------------------------------------')
    if len(task_errors) > 0:
        print('Next errors occurred:')
        for error in task_errors:
            print(error)
        print('----------------------------------------------------------------------------------------')


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

    mean = np.mean(required_days_for_emulations)
    std = np.std(required_days_for_emulations)

    _print_normal_distribution(mean, std, 'Monte Carlo emulation')
