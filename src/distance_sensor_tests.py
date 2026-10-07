import time


def distance_callback(distance):
    print(f"Distance: {distance} mm")


def run_distance_sensor_tests(ep_robot):

    ep_sensor = ep_robot.sensor
    ep_sensor.sub_distance(freq=5, callback=distance_callback)
    try:
        time.sleep(10)
    finally:
        ep_sensor.unsub_distance()
        ep_robot.close()