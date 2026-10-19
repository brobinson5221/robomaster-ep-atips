# from blaster_tests import run_blaster_tests
# from chassis_tests import run_chassis_tests
# from led_tests import run_led_tests

from robomaster_runtime import robot
from tests.chassis_tests import run_chassis_tests_with_blaster

if __name__ == "__main__":
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")
    ep_chassis = ep_robot.chassis
    ep_blaster = ep_robot.blaster
    ep_gimbal = ep_robot.gimbal

    DISTANCE_LIMIT = 400  # mm

    try:
        print(f"Robot version: {ep_robot.get_version()}")
        print(f"Robot SN: {ep_robot.get_sn()}")
        ep_robot.set_robot_mode(mode=robot.CHASSIS_LEAD)
        run_chassis_tests_with_blaster(ep_robot)
    finally:
        ep_robot.close()
