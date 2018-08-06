import work_emulator
import scipy.stats as stats

def calculate_mean(task):
    return (task[1] + 4 * task[2] + task[3]) / 6

def calculate_std(task):
    return (task[3] - task[1]) / 6

def buil_task_with_probability(task):
    return [task[0], calculate_mean(task), calculate_std(task)]

def buil_tasks_with_probability(full_estimated_df):
    return [buil_task_with_probability(task) for task in full_estimated_df[['id', 'min', 'normal', 'max']].values]

def build_generation(full_estimated_df):
    def build_task_generation(task):
        return [task[0], max(0., round(stats.norm.rvs(task[1], task[2], size=1)[0]))]
    
    return [build_task_generation(task) for task in buil_tasks_with_probability(full_estimated_df)]

def run_simulation(number_of_devs, number_of_simulations, full_estimated_df, estimated_G):
    return [work_emulator.calculate_requered_days(number_of_devs, build_generation(full_estimated_df), estimated_G) for i in range(number_of_simulations)]