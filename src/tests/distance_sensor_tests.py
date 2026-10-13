import time


def run_distance_sensor_tests(ep_robot):
    sensor_value = None
    sensor_value_list = []

    def distance_callback(distance):
        nonlocal sensor_value
        sensor_value = distance[0]
        print(f"Distance callback triggered: {sensor_value} mm")
        sensor_value_list.append(sensor_value)

    ep_sensor = ep_robot.sensor
    # ep_chassis = ep_robot.chassis
    ep_sensor.sub_distance(freq=1, callback=distance_callback)
    try:
        # Set a deadline for 5 seconds from now
        deadline = time.monotonic() + 5
        # Wait until we get a sensor value or the deadline is reached
        while sensor_value is None and time.monotonic() < deadline:
            # Wait for a short period to avoid busy waiting
            time.sleep(0.05)
        if sensor_value is not None:
            print(f"Latest distance: {sensor_value} mm")
            print(f"Sensor value list: {sensor_value_list}")
            # ep_chassis.move(x=sensor_value, y=0, z=0, xy_speed=0.1).wait_for_completed()
        else:
            print("No distance reading available.")
    finally:
        # Unsubscribe from the distance sensor to clean up resources
        if sensor_value is not None:
            ep_sensor.unsub_distance()
