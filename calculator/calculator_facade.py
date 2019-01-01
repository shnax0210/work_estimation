import numpy as np
import math
import scipy.stats as stats

from calculator.normal_distribution import NormalDistribution


def calculate_sum_normal_distribution_by_three_points(three_points_array, number_of_points=50):
    total_mean = sum([_calculate_mean_by_three_points(three_points) for three_points in three_points_array])
    total_std = math.sqrt(sum([_calculate_std_by_three_points(three_points) for three_points in three_points_array]))

    return _calculate_normal_distribution_by_mean_and_std(total_mean, total_std, number_of_points)


def calculate_normal_distribution_by_three_points(three_points, number_of_points=50):
    mean = _calculate_mean_by_three_points(three_points)
    std = _calculate_std_by_three_points(three_points)

    return _calculate_normal_distribution_by_mean_and_std(mean, std, number_of_points)


def calculate_normal_distribution_by_x(x, number_of_points=50):
    return _calculate_normal_distribution_by_mean_and_std(np.mean(x), np.std(x), number_of_points)


def calculate_mean_by_three_points(minimum, normal, maximum):
    return (minimum + 4 * normal + maximum) / 6


def calculate_std_by_three_points(minimum, maximum):
    return (maximum - minimum) / 6


def _calculate_normal_distribution_by_mean_and_std(mean, std, number_of_points):
    min_x = int(round((mean - 4 * std)))
    max_x = int(round((mean + 4 * std)))

    x = np.linspace(min_x, max_x, number_of_points)
    y = stats.norm.cdf(x, mean, std)

    return NormalDistribution(mean, std, min_x, max_x, x, y)


def _calculate_std_by_three_points(three_points):
    return calculate_std_by_three_points(three_points.minimum, three_points.maximum)


def _calculate_mean_by_three_points(three_points):
    return calculate_mean_by_three_points(three_points.minimum, three_points.normal, three_points.maximum)
