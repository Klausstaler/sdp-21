from enum import Enum
class TaskType(Enum):
    PICKUP_PARCEL = "pickup_parcel"
    RAISE_PLATFORM = "raise_platform"
    REACH_NODE = "reach_node"
    NO_TASK = "NO_TASK"
    TURN_UNTIL = "turn_until"
class Task:
    def __init__(self, task_type: TaskType, params: dict):
        self.params = params
        self.task_type = task_type
    
class Tasks:
    def __init__(self, robot_controller) -> None:
        self.params = None
        self.task_func = None
        self.robot_controller = robot_controller

    def set_task(self, task_type: TaskType):
        if task_type == TaskType.REACH_NODE:
            self.task_func = self.robot_controller.reach_node#(params["node"])
        elif task_type == TaskType.TURN_UNTIL:
            self.task_func = self.robot_controller.turn_until#(int(params["n"]))
        elif task_type == TaskType.PICKUP_PARCEL:
            self.task_func = self.robot_controller.arm.try_pickup#()
        elif task_type == TaskType.RAISE_PLATFORM:
            self.task_func = self.robot_controller.raise_platform#(**params)
    
    def call_next_task(self, task_type: TaskType, params: dict):
        self.set_task(task_type)
        success = self.task_func(**params)
        return success



def resolve_task(data: str) -> Task:
    task_type_mapper = {
        "reach_node": TaskType.REACH_NODE,
        "pickup_parcel": TaskType.PICKUP_PARCEL,
        "raise_platform": TaskType.RAISE_PLATFORM,
        "turn_until": TaskType.TURN_UNTIL,
        }
    length, robot_id, function, *params = data.split(":")
    param_dict = dict()
    for param in params:
        param = param.strip()
        if param:
            key, val = param.strip().split(",")
            param_dict[key] = val
    return Task(task_type_mapper[function], param_dict)