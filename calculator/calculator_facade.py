def calculate_task_mean_and_std(task_row):
    mean = (task_row.min_estimate + 4 * task_row.normal_estimate + task_row.max_estimate) / 6
    std = (task_row.max_estimate - task_row.min_estimate) / 6

    return mean, std
