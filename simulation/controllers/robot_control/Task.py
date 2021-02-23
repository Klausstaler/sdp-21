from enum import Enum


class TaskType(Enum):
    PICKUP_PARCEL = "pickup_parcel"
    RAISE_PLATFORM = "raise_platform"
    NO_TASK = "NO_TASK"


class Task:
    def __init__(self, task_type: TaskType, params: dict):
        self.params = params
        self.task_type = task_type


def resolve_task(data: str) -> Task:
    task_type_mapper = {"pickup_parcel": TaskType.PICKUP_PARCEL, "raise_platform": TaskType.RAISE_PLATFORM}
    length, robot_id, function, *params = data.split(":")
    param_dict = dict()
    for param in params:
        param = param.strip()
        if param:
            key, val = param.strip().split(",")
            param_dict[key] = val
    return Task(task_type_mapper[function], param_dict)
