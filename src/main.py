# from blaster_tests import run_blaster_tests
# from chassis_tests import run_chassis_tests
# from led_tests import run_led_tests
import time

from robomaster_runtime import robot
from tests.distance_sensor_tests import read_distance

if __name__ == "__main__":
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")
    ep_chassis = ep_robot.chassis

    DISTANCE_LIMIT = 400  # mm

    try:
        print(f"Robot version: {ep_robot.get_version()}")
        print(f"Robot SN: {ep_robot.get_sn()}")

        ep_robot.set_robot_mode(mode=robot.CHASSIS_LEAD)
        current_distance = read_distance(ep_robot)
        while current_distance is not None and current_distance > DISTANCE_LIMIT:
            if current_distance is not None:
                print(f"Distance: {current_distance} mm")
                ep_chassis.drive_speed(x=-0.1, y=0, z=0)
            else:
                print("No distance reading available.")
            current_distance = read_distance(ep_robot)
            if current_distance is not None and current_distance < DISTANCE_LIMIT:
                # ep_chassis.drive_speed(x=0, y=0, z=60)
                ep_chassis.drive_speed(x=0, y=0, z=60)
                time.sleep(3)
                break
    finally:
        ep_robot.close()
