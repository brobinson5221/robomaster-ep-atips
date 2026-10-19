# from blaster_tests import run_blaster_tests
# from chassis_tests import run_chassis_tests
# from led_tests import run_led_tests

from robomaster_runtime import robot
from sensor_mapping.data_collecting import collect_data, plot_data

DISTANCE_LIMIT = 400


def main():
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    try:
        print(f"Robot version: {ep_robot.get_version()}")
        print(f"Robot SN: {ep_robot.get_sn()}")
        ep_robot.set_robot_mode(mode=robot.FREE)
        ep_robot.gimbal.moveto(pitch=0, yaw=0).wait_for_completed()
        measurements = collect_data(ep_robot)
        plot_data(measurements)
    finally:
        ep_robot.close()


if __name__ == "__main__":
    main()
