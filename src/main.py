from blaster_tests import run_blaster_tests
from chassis_tests import run_chassis_tests
from led_tests import run_led_tests
from robomaster_runtime import robot

if __name__ == "__main__":
    run_led_tests()
    run_blaster_tests()
    run_chassis_tests()
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    # Get the robot's version
    ep_version = ep_robot.get_version()
    print(f"Robot version: {ep_version}")

    # Get the robot's serial number
    SN = ep_robot.get_sn()
    print(f"Robot SN: {SN}")

    ep_robot.set_robot_mode(mode=robot.GIMBAL_LEAD)

    ep_robot.close()
