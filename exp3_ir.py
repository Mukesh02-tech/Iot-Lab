import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time

# IR sensor
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.IN)

# ThingSpeak MQTT details
BROKER = "mqtt3.thingspeak.com"
CLIENT_ID = "NCgXGTEbGw8LIAsqBR4tKQM"
USERNAME = "NCgXGTEbGw8LIAsqBR4tKQM"
PASSWORD = "AmyP1wTfdDKDlTXm7tH2GG6L"
CHANNEL_ID = "3509079"

# MQTT
client = mqtt.Client(client_id=CLIENT_ID)
client.username_pw_set(USERNAME, PASSWORD)
client.connect(BROKER, 1883)

topic = "channels/" + CHANNEL_ID + "/publish"

print("IR Sensor started")

while True:

    value = GPIO.input(18)

    if value == 0:
        print("Object Detected")
    else:
        print("Object Not Detected")

    payload = "field1=" + str(value)

    client.publish(topic, payload)

    print("Sent to ThingSpeak:", value)

    time.sleep(5)