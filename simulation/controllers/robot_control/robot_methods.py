from RobotController import RobotController

def raise_platform(robot: RobotController, height: str) -> bool:
    height = float(height)
    robot.lift_motor.setPosition(height)
    return abs(robot.lift_motor.getPositionSensor().getValue() - height) < 0.001
