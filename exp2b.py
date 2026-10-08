import RPi.GPIO as GPIO 
import time 
# Define GPIO pins 
TRIG = 13
ECHO = 11 
GPIO.setmode(GPIO.BOARD) 
# Set up GPIO pins 
GPIO.setup(TRIG, GPIO.OUT) 
GPIO.setup(ECHO, GPIO.IN) 
try: 
    while True: 
        print("Distance measurement in progress") 
        # Trigger pulse (LOW initially) 
        GPIO.output(TRIG, False) 
        # Time for sensor stabilization 
        time.sleep(2) 
 
        # Set trigger pin HIGH for 10 µs 
        GPIO.output(TRIG, True) 
        time.sleep(0.00001) 
        GPIO.output(TRIG, False) 
        # Measure echo pulse 
        while GPIO.input(ECHO) == 0: 
            pulse_start = time.time() 
        while GPIO.input(ECHO) == 1: 
            pulse_end = time.time() 
        pulse_duration = pulse_end - pulse_start 
        # Calculate distance 
        distance = pulse_duration * 17150 
        distance = round(distance, 2) 
        print("Distance:", distance, "cm") 
        time.sleep(2) 
except KeyboardInterrupt: 
    # Clean up on exit 
    GPIO.cleanup()