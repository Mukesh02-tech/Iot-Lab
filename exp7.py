import RPi.GPIO as GPIO
import time
TRIG = 19
ECHO = 26
LED = 5
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)
try:
    while True:
        GPIO.output(TRIG, 1)
        time.sleep(0.00001)
        GPIO.output(TRIG, 0)
        while not GPIO.input(ECHO):
            start = time.time()
        while GPIO.input(ECHO):
            end = time.time()
        distance = (end - start) * 17150
        print("Distance:", round(distance, 2), "cm")

        GPIO.output(LED, distance < 20)
        time.sleep(0.2)

except KeyboardInterrupt:
    GPIO.cleanup()