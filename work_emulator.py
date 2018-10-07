def calculate_requered_days(number_of_workers, all_tasks, graph, print_info=False):
    def create_workers(number):
        return [{'task': None, 'left_days': 0} for index in range(number)]

    workers = create_workers(number_of_workers)
    days = 0

    in_progress_tasks = set()
    completed_tasks = set()
    completed_tasks.add('ProjectStart')
    all_task_names = set([task[0] for task in all_tasks])

    for task in all_tasks:
        if task[1] == 0.0:
            completed_tasks.add(task[0])

    def update_workers():
        for worker in workers:
            if worker['task'] is not None:
                worker['left_days'] = worker['left_days'] - 1
                if (worker['left_days'] == 0):
                    completed_tasks.add(worker['task'])
                    in_progress_tasks.remove(worker['task'])
                    worker['task'] = None

    def find_free_workers():
        return [worker for worker in workers if worker['task'] is None]

    def is_not_blocked(task_name):
        for blocker in graph.predecessors(task_name):
            if blocker not in completed_tasks and blocker in all_task_names:
                return False

        return True

    def find_task(task_name):
        return [task for task in all_tasks if task[0] == str(task_name)][0]

    def find_task_value(task):
        task_value = task[1]

        for sub_task_name in graph.successors(task[0]):
            if sub_task_name != task[0]:
                task_value = task_value + find_task_value(find_task(sub_task_name))

        return task_value

    def find_best_task(tasks_to_pick):
        best_task = tasks_to_pick[0]
        best_task_value = find_task_value(best_task)

        for task in tasks_to_pick:
            task_value = find_task_value(task)
            if (task_value > best_task_value):
                best_task = task
                best_task_value = task_value

        return best_task

    def find_free_task():
        all_free_tasks = [task for task in all_tasks if
                          task[0] not in in_progress_tasks and task[0] not in completed_tasks]
        all_free_not_blocked_tasks = [task for task in all_free_tasks if is_not_blocked(task[0])]

        if (len(all_free_not_blocked_tasks) == 0):
            return None

        return find_best_task(all_free_not_blocked_tasks)

    def assin_worker_to_task(worker, task):
        worker['task'] = task[0]
        worker['left_days'] = task[1]
        in_progress_tasks.add(task[0])

    while True:
        if print_info:
            print(in_progress_tasks)
        days = days + 1
        update_workers()
        free_workers = find_free_workers()

        for worker in free_workers:
            free_task = find_free_task()
            if free_task is not None:
                assin_worker_to_task(worker, free_task)
            else:
                break
        if (len(completed_tasks) == len(all_tasks)):
            break

    return days
