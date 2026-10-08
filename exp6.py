import RPi.GPIO as GPIO
import requests
import time

LED = 18

TOKEN = "qAgA3-nG5ssWAIY9JUOhlABu41O_9vB_"
URL = "https://blynk.cloud/external/api/get"

GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED, GPIO.OUT)

print("Blynk IoT Actuator Control Started")
print("----------------------------------")

try:
    while True:

        try:
            response = requests.get(
                URL,
                params={
                    "token": TOKEN,
                    "v0": ""
                },
                timeout=10
            )

            if response.status_code == 200:

                value = int(response.text.strip())

                if value == 1:
                    GPIO.output(LED, GPIO.HIGH)
                    print("Blynk Switch : ON")
                    print("LED          : ON")

                else:
                    GPIO.output(LED, GPIO.LOW)
                    print("Blynk Switch : OFF")
                    print("LED          : OFF")

            else:
                print("Blynk Error:", response.status_code)

        except requests.exceptions.Timeout:
            print("Connection timeout - retrying...")

        except requests.exceptions.RequestException as e:
            print("Connection error:", e)

        print("----------------------------------")
        time.sleep(2)

except KeyboardInterrupt:
    print("Program stopped.")

finally:
    GPIO.output(LED, GPIO.LOW)
    GPIO.cleanup()