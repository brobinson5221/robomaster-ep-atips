import math

import matplotlib.pyplot as plt

from tests.distance_sensor_tests import read_distance

DISTANCE_MAX = 4000
DISTANCE_MIN = 100

def collect_data(ep_robot):
    measurements = []

    ep_gimbal = ep_robot.gimbal
    for angle in range(-180, 180, 5):
        ep_gimbal.moveto(pitch=0, yaw=angle).wait_for_completed()

        distance = read_distance(ep_robot)

        if distance is not None and DISTANCE_MIN <= distance <= DISTANCE_MAX:
            measurements.append((angle, distance))
    return measurements
