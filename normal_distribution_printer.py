import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import math


def print_normal_distribution(mean, std, title):
    def find_cell_size(min, max):
        max_number_of_cells = 15

        if (max - min) > max_number_of_cells:
            return (max - min) // max_number_of_cells

        return 1

    min = int(round((mean - 4 * std)))
    max = int(round((mean + 4 * std)))

    x = np.linspace(min, max, 50)
    y = stats.norm.cdf(x, mean, std)

    fig = plt.figure()
    ax = fig.gca()
    ax.set_xticks(np.arange(min, max, find_cell_size(min, max)))
    ax.set_yticks(np.arange(0, 1.1, 0.1))
    fig.suptitle(title, fontsize=14)
    plt.xlabel('Estimate', fontsize=14)
    plt.ylabel('Probability', fontsize=14)

    plt.plot(x, y)
    plt.grid()
    plt.show()


def _calculate_mean(task):
    return (task.min_estimate + 4 * task.normal_estimate + task.max_estimate) / 6


def _calculate_std(task):
    return (task.max_estimate - task.min_estimate) / 6


def _build_title(task):
    if task.name:
        return "{}:{}".format(task.uid, task.name)
    else:
        return task.uid


def print_normal_distribution_for_task(task):
    print_normal_distribution(_calculate_mean(task), _calculate_std(task), _build_title(task))


def print_normal_distribution_for_tasks(tasks):
    total_mean = sum([_calculate_mean(task) for task in tasks])
    total_std = math.sqrt(sum([std * std for std in [_calculate_std(task) for task in tasks]]))

    print_normal_distribution(total_mean, total_std, 'Total')
