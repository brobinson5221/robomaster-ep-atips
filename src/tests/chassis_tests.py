import time

from robomaster import led

from robomaster_runtime import robot
from tests.distance_sensor_tests import read_distance

DISTANCE_LIMIT = 360  # mm


def run_chassis_tests(ep_robot):

    ep_chassis = ep_robot.chassis
    ep_chassis.drive_speed(x=-1.0, y=0, z=0)
    time.sleep(3)

    ep_chassis.drive_speed(x=0, y=1.0, z=0)
    time.sleep(3)

    ep_chassis.drive_speed(x=0, y=0, z=60)
    time.sleep(3)


def run_chassis_tests_with_blaster(ep_robot):

    ep_chassis = ep_robot.chassis
    ep_gimbal = ep_robot.gimbal
    ep_blaster = ep_robot.blaster
    ep_led = ep_robot.led
    current_distance = read_distance(ep_robot)
    time.sleep(1)  # Allow time for the distance sensor to stabilize
    counter = 0
    ep_led.set_led(comp=led.COMP_ALL, r=255, g=0, b=0, effect=led.EFFECT_ON)
    while current_distance is not None and current_distance > DISTANCE_LIMIT:
        if current_distance is not None:
            print(f"Distance: {current_distance} mm")
            ep_chassis.drive_speed(x=-0.1, y=0, z=0)
            counter += 1
        else:
            print("No distance reading available.")
        current_distance = read_distance(ep_robot)
        if current_distance is not None and current_distance < DISTANCE_LIMIT:
            ep_chassis.drive_speed(x=0, y=0, z=0)
            time.sleep(1)
            ep_robot.set_robot_mode(mode=robot.FREE)
            time.sleep(1)
            ep_gimbal.moveto(pitch=10, yaw=90).wait_for_completed()
            time.sleep(1)
            ep_blaster.fire(times=1)
            time.sleep(2)
            ep_gimbal.moveto(pitch=20, yaw=-90).wait_for_completed()
            time.sleep(1)
            ep_blaster.fire(times=1)
            time.sleep(2)
            ep_gimbal.moveto(pitch=0, yaw=0).wait_for_completed()
            ep_robot.set_robot_mode(mode=robot.CHASSIS_LEAD)
            time.sleep(1)
            break
    # ep_gimbal.moveto(pitch=0, yaw=90).wait_for_completed()
    ep_led.set_led(comp=led.COMP_ALL, r=0, g=255, b=0, effect=led.EFFECT_ON)
    ep_chassis.move(x=0, y=0, z=-8, z_speed=30).wait_for_completed()
    while counter > 0:
        ep_chassis.drive_speed(x=0.1, y=0, z=0)
        counter -= 1
        print(f"Returning to original position, steps remaining: {counter}")
        time.sleep(1)
    ep_led.set_led(comp=led.COMP_ALL, r=0, g=0, b=255, effect=led.EFFECT_ON)
    ep_chassis.drive_speed(x=0, y=0, z=0)
