import time

from tests.distance_sensor_tests import read_distance

DISTANCE_LIMIT = 400  # mm


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
    ep_blaster = ep_robot.blaster
    current_distance = read_distance(ep_robot)
    counter = 0
    while current_distance is not None and current_distance > DISTANCE_LIMIT:
        if current_distance is not None:
            print(f"Distance: {current_distance} mm")
            ep_chassis.drive_speed(x=-0.1, y=0, z=0)
            counter += 1
        else:
            print("No distance reading available.")
        current_distance = read_distance(ep_robot)
        if current_distance is not None and current_distance < DISTANCE_LIMIT:
            # ep_chassis.drive_speed(x=0, y=0, z=60)
            ep_chassis.drive_speed(x=0, y=0, z=60)
            time.sleep(3)
            break
    counter -= 1
    while counter > 0:
        ep_chassis.drive_speed(x=-0.1, y=0, z=0)
        counter -= 1
        print(f"Returning to original position, steps remaining: {counter}")
        time.sleep(1)
    ep_chassis.drive_speed(x=0, y=0, z=30)
    time.sleep(3)
    ep_blaster.fire(times=2)
    ep_chassis.drive_speed(x=0, y=0, z=-60)
    time.sleep(3)
    ep_blaster.fire(times=2)
