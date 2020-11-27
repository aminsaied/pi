import RPi.GPIO as GPIO
import time

# use broadcomm GPIO naming schema
GPIO.setmode(GPIO.BCM)

# setup GPIO pin 18 as an output
GPIO.setup(18, GPIO.OUT)

# start with LED off
GPIO.output(18, GPIO.LOW)

state = 0
while True:
    in_ = input()
    
    if in_ == 'x':
        break

    try:
        c = int(in_)
    except:
        c = 1


    for _ in range(2 * c):
        
        if state == 0:
            GPIO.output(18, GPIO.HIGH)
            state = 1
        else:
            GPIO.output(18, GPIO.LOW)
            state = 0
        time.sleep(0.1)


# clean up at end of program
GPIO.cleanup()
