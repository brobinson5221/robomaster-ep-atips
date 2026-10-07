import time

from robomaster import led


def run_led_tests(ep_robot):

    ep_led = ep_robot.led
    ep_led.set_led(comp=led.COMP_ALL, r=255, g=219, b=187, effect=led.EFFECT_ON)

    bright = 1
    for i in range(8):
        print(f"Setting brightness to: {bright << i}")
        ep_led.set_led(
            comp=led.COMP_ALL,
            r=bright << i,
            g=bright << i,
            b=bright << i,
            effect=led.EFFECT_ON,
        )
        time.sleep(1)
        print(f"brightness: {bright << i}")
