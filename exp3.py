import paho.mqtt.client as mqtt
BROKER = "mqtt3.thingspeak.com"
CLIENT_ID = "FBUdNTMjBhw8JAoEIwgeATo"
USERNAME = "FBUdNTMjBhw8JAoEIwgeATo"
PASSWORD = "ptSHUcC2DP9PzMEsSvrXc1GJ"
CHANNEL_ID = "3525475"
client = mqtt.Client(client_id=CLIENT_ID)
client.username_pw_set(USERNAME, PASSWORD)
client.connect(BROKER, 1883)  
topic = "channels/" + CHANNEL_ID + "/publish"
while True:
    value = float(input("Enter Sensor Value: "))
    payload = "field1=" + str(value)
    client.publish(topic, payload)
    print("Published:", payload)
    choice = input("Do you want to publish another value? (y/n): ")
    if choice.lower() != 'y':
        break
client.disconnect()