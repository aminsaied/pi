import RPi.GPIO as GPIO
import time

class LEDController:

    def __init__(self):

        # use broadcomm GPIO naming schema
        GPIO.setmode(GPIO.BCM)

        # setup GPIO pin 18 as an output
        GPIO.setup(18, GPIO.OUT)

        # start with LED off
        GPIO.output(18, GPIO.LOW)

        # main
        GPIO.output(18, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(18, GPIO.LOW)

        # clean up at end of program
        GPIO.cleanup()
