from threading import Event


def read_distance(ep_robot, timeout=5):
    """Return the first sensor's next distance in mm, or None on timeout."""
    sensor_value = None
    # The callback signals this event when a reading is available.
    reading_ready = Event()

    def distance_callback(distance):
        # Update the variable in read_distance()
        nonlocal sensor_value
        # Keep only the first reading
        if sensor_value is None:
            # Get the first sensor's distance in mm.
            sensor_value = distance[0]
            reading_ready.set()

    ep_sensor = ep_robot.sensor
    # Request distance updates once per second.
    ep_sensor.sub_distance(freq=1, callback=distance_callback)
    try:
        # Wait without polling, up to timeout seconds.
        if reading_ready.wait(timeout):
            return sensor_value
        # No reading arrived before the timeout.
        return None
    finally:
        # Stop updates whether we received a reading or timed out.
        ep_sensor.unsub_distance()


def run_distance_sensor_tests(ep_robot):
    sensor_value = read_distance(ep_robot)
    # Check against None
    if sensor_value is not None:
        print(f"Distance: {sensor_value} mm")
    else:
        print("No distance reading available.")
