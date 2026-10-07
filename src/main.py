# from blaster_tests import run_blaster_tests
# from chassis_tests import run_chassis_tests
# from led_tests import run_led_tests
from distance_sensor_tests import run_distance_sensor_tests
from robomaster_runtime import robot

if __name__ == "__main__":
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    try:
        print(f"Robot version: {ep_robot.get_version()}")
        print(f"Robot SN: {ep_robot.get_sn()}")

        ep_robot.set_robot_mode(mode=robot.GIMBAL_LEAD)
        run_distance_sensor_tests(ep_robot)
    finally:
        ep_robot.close()
