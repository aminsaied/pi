import RPi.GPIO as GPIO
import time

# use broadcomm GPIO naming schema
GPIO.setmode(GPIO.BCM)

# setup GPIO pin 18 as an output
GPIO.setup(17, GPIO.IN)
GPIO.setup(18, GPIO.OUT)

# start with LED off
GPIO.output(18, GPIO.LOW)

while True:
    res = GPIO.input(17)
    if res == 1:
        GPIO.output(18, GPIO.HIGH)
        print(res, 'on')
    else:
        GPIO.output(18, GPIO.LOW)
        print(res, 'off')
    time.sleep(3)


# clean up at end of program
GPIO.cleanup()
