from enum import Enum

class TaskType(Enum):
    PICKUP_PARCEL = "pickup_parcel"
    RAISE_PLATFORM = "raise_platform"

class Task:
    def __init__(self, task_type: TaskType, params: dict):
        self.params = params
        self.task_type = task_type