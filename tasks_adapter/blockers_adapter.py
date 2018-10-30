def adapt_blockers(task_rows, tasks):
    uid_to_task_row = dict([(task_row.uid, task_row) for task_row in task_rows])
    uid_to_task = dict([(task.uid, task) for task in tasks])

    for task in tasks:
        for blocker_uid in uid_to_task_row[task.uid].blockers:
            task.add_blocker(uid_to_task[blocker_uid])


def validate_blockers(task_rows):
    valid_task_rows = []
    errors = []

    uid_to_task_row = dict([(task_row.uid, task_row) for task_row in task_rows])

    for task_row in task_rows:
        task_errors = _validate_task_blockers(task_row, uid_to_task_row, [])
        if len(task_errors) > 0:
            errors.extend(task_errors)
        else:
            valid_task_rows.append(task_row)

    return valid_task_rows, errors


def _validate_task_blockers(task_row, uid_to_task_row, tasks_chain):
    errors = []
    tasks_chain.append(task_row.uid)

    for blocker_uid in task_row.blockers:
        new_tasks_chain = tasks_chain.copy()
        if blocker_uid in uid_to_task_row:
            errors.extend(_validate_task_blockers(uid_to_task_row[blocker_uid], uid_to_task_row, new_tasks_chain))
        else:
            new_tasks_chain.append(blocker_uid)
            errors.append(_create_error_message(new_tasks_chain))

    return errors


def _create_error_message(new_tasks_chain):
    return "Task {} filtered due to missing of last blocker in chain: {}".format(new_tasks_chain[0],
                                                                                 new_tasks_chain[1:])
