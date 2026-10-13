import time


def run_chassis_tests(ep_robot):

    ep_chassis = ep_robot.chassis
    ep_chassis.drive_speed(x=-1.0, y=0, z=0)
    time.sleep(3)

    ep_chassis.drive_speed(x=0, y=1.0, z=0)
    time.sleep(3)

    ep_chassis.drive_speed(x=0, y=0, z=60)
    time.sleep(3)
