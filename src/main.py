from robomaster import led

from robomaster_runtime import robot

if __name__ == "__main__":
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    # Get the robot's version
    ep_version = ep_robot.get_version()
    print(f"Robot version: {ep_version}")

    # Get the robot's serial number
    SN = ep_robot.get_sn()
    print(f"Robot SN: {SN}")

    ep_robot.set_robot_mode(mode=robot.GIMBAL_LEAD)

    ep_led = ep_robot.led
    ep_led.set_led(comp=led.COMP_ALL, r=255, g=219, b=187, effect=led.EFFECT_ON)

    ep_robot.close()
