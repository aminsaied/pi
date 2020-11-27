import RPi.GPIO as GPIO
import time

LED = 18

# use broadcomm GPIO naming schema
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)

GPIO.output(LED, GPIO.HIGH)
time.sleep(20)
GPIO.output(LED, GPIO.LOW)

# clean up at end of program
GPIO.cleanup()
