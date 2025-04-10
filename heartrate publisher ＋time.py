import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

BROKER_ADDRESS = "112.74.107.115"

BROKER_PORT = 1883

client = mqtt.Client()

client.connect(BROKER_ADDRESS, BROKER_PORT)
client.loop_start()

try:
    while True:
        temp = random.uniform(50, 120)  # 生成随机心率 (50 ~ 120)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 记录当前时间
        data = {"temp": temp, "timestamp": timestamp}  # 发送时间戳
        payload = json.dumps(data)
        result = client.publish("health/wearable/heart rate", payload, qos=1)
        status = result[0]
        if status == 0:
            print(f"Message sent at {timestamp}: {payload}")
        else:
            print("Failed to send message!")

        time.sleep(5)

except KeyboardInterrupt:
    pass
finally:
    client.loop_stop()
    client.disconnect()

