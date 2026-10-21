import math

import matplotlib.pyplot as plt
from matplotlib.markers import MarkerStyle
from matplotlib.projections.polar import PolarAxes

from tests.distance_sensor_tests import read_distance

DISTANCE_MAX = 4000
DISTANCE_MIN = 100
MAX_ANGLE_GAP_DEG = 5
MAX_POINT_GAP_MM = 500
MAX_RANGE_JUMP_MM = 300


def collect_data(ep_robot):
    measurements = []
    ep_gimbal = ep_robot.gimbal

    for angle in range(-180, 180, 5):
        ep_gimbal.moveto(pitch=0, yaw=angle).wait_for_completed()

        distance = read_distance(ep_robot)

        if distance is not None and DISTANCE_MIN <= distance <= DISTANCE_MAX:
            measurements.append((angle, distance))
    return measurements


def plot_data(measurements):
    _, ax = plt.subplots(subplot_kw={"projection": "polar"})
    if isinstance(ax, PolarAxes):
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)
    angles = [math.radians(angle) for angle, _ in measurements]
    distances = [distance / 1000 for _, distance in measurements]
    ax.scatter(angles, distances)

    # Only join neighboring scan directions that could belong to one surface.
    ordered = sorted(measurements)
    for (angle1, distance1), (angle2, distance2) in zip(ordered, ordered[1:] + ordered[:1]):
        # Modulo also checks the last-to-first pair across the back of a full scan.
        angle_gap = (angle2 - angle1) % 360
        if not 0 < angle_gap <= MAX_ANGLE_GAP_DEG:
            continue
        if abs(distance2 - distance1) > MAX_RANGE_JUMP_MM:
            continue

        # Physical separation matters too, since rays spread out with distance.
        point_gap = math.hypot(
            distance2 * math.sin(math.radians(angle2)) - distance1 * math.sin(math.radians(angle1)),
            distance2 * math.cos(math.radians(angle2)) - distance1 * math.cos(math.radians(angle1)),
        )
        if point_gap <= MAX_POINT_GAP_MM:
            ax.plot(
                [math.radians(angle1), math.radians(angle2)],
                [distance1 / 1000, distance2 / 1000],
                color="C0",
                linewidth=1.5,
                zorder=1,
            )

    if measurements:
        nearest_angle, nearest_distance = min(measurements, key=lambda measurement: measurement[1])
        ax.scatter(
            [math.radians(nearest_angle)],
            [nearest_distance / 1000],
            color="red",
            marker=MarkerStyle("*"),
            s=180,
            zorder=3,
            label=f"Nearest: {nearest_distance:.0f} mm at {nearest_angle:g} degrees",
        )
        ax.legend()

    plt.show()


def shoot_nearest_target(ep_robot, measurements):
    if measurements:
        nearest_angle, _ = min(measurements, key=lambda measurement: measurement[1])
        ep_robot.gimbal.moveto(pitch=0, yaw=nearest_angle).wait_for_completed()
        ep_robot.blaster.fire(times=1)
