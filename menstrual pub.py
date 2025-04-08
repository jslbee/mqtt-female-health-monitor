import paho.mqtt.client as mqtt
import json
import time
import random

# Broker details
BROKER_ADDRESS = "120.76.249.191"
BROKER_PORT = 1883

# Create a client instance
client = mqtt.Client()

# Connect to the broker
client.connect(BROKER_ADDRESS, BROKER_PORT)
client.loop_start()

# Check menstrual condition
def check_menstrual_cycle(duration):
    if duration < 5:
        condition = "Caution! You may be so stressed these days!"
    elif 5 <= duration <= 7:
        condition = "Great condition! Keep going girl!"
    else:
        condition = "Caution! Your body may seek for some help!"
    return condition

# Publish messages in a loop
try:
    while True:
        # random data
        duration = round(random.uniform(3, 8))

        condition = check_menstrual_cycle(duration)

        data = {
            "duration": duration,
            "condition": condition
        }

        payload = json.dumps(data)

        # publish to health/userinput/menstrual_cycle
        client.publish("health/userinput/menstrual_cycle", payload, qos=1)

        print("\nSensor published:", payload)

        time.sleep(5)

except KeyboardInterrupt:
    pass


finally:
    client.loop_stop()
    client.disconnect()

    