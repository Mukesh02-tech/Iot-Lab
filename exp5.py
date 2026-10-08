import RPi.GPIO as GPIO
import time
import requests

# GPIO pins - PHYSICAL PIN NUMBERS
TRIG = 13
ECHO = 11

# Google Apps Script URL
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzGmFDOpzw1HWHBWecX-lBx2JqbXZh4eB3ntNkMKGw6tKYz4IJ362pb_Q4-yy_R37Av/exec"

# Threshold
THRESHOLD = 20

GPIO.setmode(GPIO.BOARD)

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

try:

    while True:

        print("Distance measurement in progress")

        # Trigger LOW
        GPIO.output(TRIG, False)
        time.sleep(2)

        # Trigger HIGH for 10 microseconds
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        # Wait for ECHO HIGH
        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()

        # Wait for ECHO LOW
        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()

        # Calculate distance
        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150
        distance = round(distance, 2)

        print("Distance:", distance, "cm")

        # Check threshold
        if distance < THRESHOLD:
            status = "OBJECT TOO CLOSE"
        else:
            status = "NORMAL"

        print("Status:", status)

        # Send to Google Sheets
        try:

            response = requests.get(
                SCRIPT_URL,
                params={"distance": distance},
                timeout=10
            )

            print("Cloud:", response.text)

        except requests.RequestException:
            print("Cloud: Transmission error")

        print("-------------------------")

        time.sleep(2)

except KeyboardInterrupt:

    print("Program stopped")

finally:

    GPIO.cleanup()