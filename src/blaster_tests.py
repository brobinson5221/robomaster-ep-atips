from robomaster import blaster

from robomaster_runtime import robot


def run_blaster_tests():
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    # Get the robot's version
    ep_version = ep_robot.get_version()
    print(f"Robot version: {ep_version}")

    # Get the robot's serial number
    serial_number = ep_robot.get_sn()
    print(f"Robot SN: {serial_number}")

    ep_robot.set_robot_mode(mode=robot.GIMBAL_LEAD)

    ep_blaster = ep_robot.blaster
    ep_blaster.fire(times=3)
