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
    ep_sensor.sub_distance(freq=5, callback=distance_callback)
    try:
        time.sleep(10)
        if sensor_value is not None:
            print(f"Latest distance: {sensor_value} mm")
            print(f"Sensor value list: {sensor_value_list}")
        else:
            print("No distance reading available.")
    finally:
        ep_sensor.unsub_distance()
        ep_robot.close()
