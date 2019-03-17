from bottle import put, post, request, run, route, static_file
import os
import uuid

import work_estimation_facade
from calculator.three_points import ThreePoints
from tasks_reader import tasks_filter
from tasks_reader.task_row import TaskRow

EXCEL_FILE_EXTENSION = '.xlsx'

TEMP_DIRECTORY = 'tmp'


@route('/application/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='ui/web/')


@put('/api/excelWorkbook')
def save_temp_excel_file():
    if not os.path.exists(TEMP_DIRECTORY):
        os.makedirs(TEMP_DIRECTORY)

    temp_file_name = str(uuid.uuid4()) + EXCEL_FILE_EXTENSION

    with open(_build_path_to_temp_file(temp_file_name), 'wb') as out:
        out.write(request.body.read())

    return {'tempFileName': temp_file_name}


@post('/api/excelWorkbook/tasks')
def load_tasks_from_temp_excel_file():
    parameters = request.json
    task_rows, errors = work_estimation_facade.read_from_excel(file=_build_path_to_temp_file(parameters["file"]),
                                                               sheet=parameters["sheet"],
                                                               first_row=parameters["first_row"],
                                                               last_row=parameters["last_row"],
                                                               columns_mapping=parameters["columns_mapping"],
                                                               rows_to_skip=parameters["rows_to_skip"],
                                                               filter_predicates=[
                                                                   tasks_filter.MinEstimateRequiredPredicate(),
                                                                   tasks_filter.NormalEstimateRequiredPredicate(),
                                                                   tasks_filter.MaxEstimateRequiredPredicate()]
                                                               )
    return {
        "tasks": _convert_task_rows(task_rows),
        "errors": errors
    }


@post('/api/tasks/normalDistribution')
def calculate_normal_distributions():
    tasks = request.json["tasks"]
    number_of_points = request.json["numberOfPoints"]

    return {
        "taskNormalDistributions": _build_normal_distributions(tasks, number_of_points)
    }


@post('/api/tasks/roadMap')
def calculate_normal_distributions():
    task_rows = _convert_to_task_rows(request.json["tasks"])
    number_of_workers = request.json["numberOfWorkers"]

    valid_tasks, task_errors, history_records = work_estimation_facade.build_road_map(task_rows, number_of_workers)

    return {
        "roadMap": _convert_history_records(history_records),
        "numberOfValidTasks": len(valid_tasks),
        "errors": task_errors
    }


def _convert_work_info(work_info):
    return {
        "worker": work_info.worker_name,
        "task_uid": work_info.task_uid
    }


def _convert_history_record(history_record):
    return {
        "day": history_record.day,
        "work": [_convert_work_info(work_info) for work_info in history_record.cells]
    }


def _convert_history_records(history_records):
    return [_convert_history_record(history_record) for history_record in history_records]


def _convert_to_task_rows(tasks):
    return [_convert_to_task_row(task) for task in tasks]


def _convert_to_task_row(task):
    return TaskRow(task['uid'], task['name'], task['blockers'], task['min_estimate'], task['normal_estimate'],
                   task['max_estimate'])


def _convert_normal_distribution(normal_distribution, task):
    return {
        "taskUid": task["uid"],
        "mean": normal_distribution.mean,
        "std": normal_distribution.std,
        "min_x": normal_distribution.min_x,
        "max_x": normal_distribution.max_x,
        "x": normal_distribution.x.tolist(),
        "y": normal_distribution.y.tolist()
    }


def _build_normal_distribution(task, number_of_points):
    three_points = _convert_task_to_three_points(task)
    normal_distributions = work_estimation_facade.calculate_normal_distribution_by_three_points(three_points,
                                                                                                number_of_points)
    return _convert_normal_distribution(normal_distributions, task)


def _build_normal_distributions(tasks, number_of_points):
    return [_build_normal_distribution(task, number_of_points) for task in tasks]


def _convert_task_to_three_points(task):
    return ThreePoints(task["min_estimate"], task["normal_estimate"], task["max_estimate"])


def _convert_task_row(task_row):
    return {
        "uid": task_row.uid,
        "name": task_row.name,
        "blockers": task_row.blockers,
        "min_estimate": task_row.min_estimate,
        "normal_estimate": task_row.normal_estimate,
        "max_estimate": task_row.max_estimate
    }


def _convert_task_rows(task_rows):
    return [_convert_task_row(task_row) for task_row in task_rows]


def _build_path_to_temp_file(temp_file_name):
    return os.path.join(TEMP_DIRECTORY, temp_file_name)


run(host='localhost', port=5000, debug=True)
