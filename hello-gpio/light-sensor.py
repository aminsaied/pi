import RPi.GPIO as GPIO
import time

LED = 18
LIGHT_SENSOR = 17

# use broadcomm GPIO naming schema
GPIO.setmode(GPIO.BCM)

# setup GPIO pin 18 as an output
GPIO.setup(LIGHT_SENSOR, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

# start with LED off
for _ in range(5):
    GPIO.output(LED, GPIO.HIGH)
    time.sleep(0.25)
    GPIO.output(LED, GPIO.LOW)
    time.sleep(0.25)

while True:
    res = GPIO.input(LIGHT_SENSOR)
    if res == 1:
        GPIO.output(LED, GPIO.HIGH)
        print(res, 'on')
    else:
        GPIO.output(LED, GPIO.LOW)
        print(res, 'off')
    time.sleep(1)


# clean up at end of program
GPIO.cleanup()
