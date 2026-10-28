# from led_tests import run_led_tests
from robomaster import led

from robomaster_runtime import robot
from sensor_mapping.data_collecting import collect_data, plot_data, shoot_nearest_target
from tests.chassis_tests import run_chassis_tests_with_blaster

DISTANCE_LIMIT = 400


def main():
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")
    ep_led = ep_robot.led
    ep_chassis = ep_robot.chassis

    try:
        print(f"Robot version: {ep_robot.get_version()}")
        print(f"Robot SN: {ep_robot.get_sn()}")
        ep_robot.set_robot_mode(mode=robot.CHASSIS_LEAD)
        ep_robot.gimbal.moveto(pitch=0, yaw=0).wait_for_completed()
        run_chassis_tests_with_blaster(ep_robot)
        measurements = collect_data(ep_robot)
        plot_data(measurements)
        ep_led.set_led(comp=led.COMP_ALL, r=255, g=255, b=0, effect=led.EFFECT_ON)
        ep_robot.gimbal.moveto(pitch=0, yaw=0).wait_for_completed()
        ep_chassis.move(x=0, y=0, z=-20, z_speed=180).wait_for_completed()
        shoot_nearest_target(ep_robot, measurements)
    finally:
        ep_robot.close()


if __name__ == "__main__":
    main()
