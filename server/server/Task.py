from enum import Enum


class TaskType(Enum):
    PICKUP_PARCEL = 1
    RAISE_PLATFORM = 2

class Task:
    def __init__(self, task_type: TaskType, params: dict):
        self.params = params
        self.task_type = task_type