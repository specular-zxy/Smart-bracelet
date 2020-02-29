# control the motor to alarm
import RPi.GPIO as GPIO
import time

class mot:
    def __initss__(self):
        # model
        GPIO.setmode(GPIO.BCM)
        # pin in GPIO PIN2
        GPIO.setup(27, GPIO.OUT, initial=GPIO.HIGH)
        # GPIO.setwarnings(False)

    def run(self):
        # mot run 3 times
        GPIO.output(27, 1)
        time.sleep(0.5)
        GPIO.output(27, 0)
        time.sleep(0.5)
        GPIO.output(27, 1)
        time.sleep(0.5)
        GPIO.output(27, 0)
        time.sleep(0.5)
        GPIO.output(27, 1)
        time.sleep(0.5)
        GPIO.output(27, 0)
        GPIO.cleanup()
        print("noticed")
