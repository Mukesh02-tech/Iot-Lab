import RPi.GPIO as GPIO 
import time 
sensor = 16 
buzzer = 18 
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD) 
GPIO.setup(sensor, GPIO.IN) 
GPIO.setup(buzzer, GPIO.OUT) 
print("IR Sensor Ready...") 
try: 
    while True: 
        if not GPIO.input(sensor): 
            print("Object Detected") 
            GPIO.output(buzzer, True) 
            time.sleep(1) 
        else: 
            GPIO.output(buzzer, False) 
 
        time.sleep(0.1) 
except KeyboardInterrupt: 
    GPIO.cleanup()