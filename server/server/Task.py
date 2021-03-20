from enum import Enum


class TaskType(Enum):
    PICKUP_PARCEL = "pickup_parcel"
    DROPOFF_PARCEL = "dropoff_parcel"
    RAISE_PLATFORM = "raise_platform"
    REACH_NODE = "reach_node"
    NO_TASK = "NO_TASK"
    TURN_UNTIL = "turn_until"
    MOVEMENT = "movement"
    MOVE_ARM = "move_arm"


identity = lambda x: x
Tasks_dic = {
    TaskType.REACH_NODE: {
        "task_func": lambda controller: controller.reach_node,
        "completition_func": lambda controller: controller.check_reach_node,
    },
    TaskType.TURN_UNTIL: {
        "task_func": lambda controller: controller.nav.turn_until_line_n,
        "completition_func": identity,
    },
    TaskType.PICKUP_PARCEL: {
        "task_func": lambda controller: controller.arm.try_pickup,
        "completition_func": identity,
    },
    TaskType.DROPOFF_PARCEL: {
        "task_func": lambda controller: controller.arm.try_dropoff,
        "completition_func": None,
    },
    TaskType.RAISE_PLATFORM: {
        "task_func": lambda controller: controller.raise_platform,
        "completition_func": identity,
    },
    TaskType.MOVEMENT: {
        "task_func": lambda controller: controller.nav.movement_wrapper,
        "completition_func": identity,
    },
    TaskType.MOVE_ARM: {
        "task_func": lambda controller: controller.arm.move_arm,
        "completition_func": identity,
    }
}


class Task:
    def __init__(self, task_type: TaskType, params: dict):
        self.params = params
        self.task_type = task_type

    def __repr__(self):
        return f"<Task type: {self.task_type.value}, Parameters {self.params}>"


def resolve_task(data: str) -> Task:
    task_type_mapper = {
        "reach_node": TaskType.REACH_NODE,
        "pickup_parcel": TaskType.PICKUP_PARCEL,
        "dropoff_parcel": TaskType.DROPOFF_PARCEL,
        "raise_platform": TaskType.RAISE_PLATFORM,
        "turn_until": TaskType.TURN_UNTIL,
        "movement": TaskType.MOVEMENT,
        "move_arm": TaskType.MOVE_ARM
    }
    length, robot_id, function, *params = data.split(":")
    param_dict = dict()
    for param in params:
        param = param.strip()
        if param:
            key, val = param.strip().split(",")
            param_dict[key] = val
    return Task(task_type_mapper[function], param_dict)
