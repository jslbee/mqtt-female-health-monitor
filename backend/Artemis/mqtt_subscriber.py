import json
import paho.mqtt.client as mqtt
from sqlalchemy.orm import Session
from app.database import SessionLocal 

try:
    from app.insert_data import save_temperature_data, save_heart_rate_data, save_menstrual_data
    print("Successfully imported insert_data module")
except ImportError as e:
    print(f"Failed to import insert_data module: {e}")

# MQTT Broker settings (replace with your own IP)
broker_address = "120.76.249.191"
port = 1883
topics = [
    ("health/wearable/temperature", 0),
    ("health/wearable/heart_rate", 0),
    ("health/userinput/menstrual_cycle", 0)
]


# MQTT connection callback
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    if rc == 0:
        print("MQTT connection successful, subscribing to topics...")
        client.subscribe(topics)
    else:
        print(f"MQTT connection failed with code: {rc}")

# MQTT message callback
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode('utf-8')
    print(f"Received message from topic '{topic}': {payload}")

    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        print(f"JSON decode error for topic {topic}: {payload}")
        return

    db: Session = SessionLocal()  # 创建一个新的会话

    try:
        if topic == "health/wearable/temperature":
            save_temperature_data(
                db,
                data.get("value"),
                data.get("warning"),
                data.get("trend")
            )
            print("Temperature data saved successfully")
        elif topic == "health/wearable/heart_rate":
            save_heart_rate_data(
                db,
                data.get("heart_rate"),
                data.get("health_status"),
                data.get("timestamp")
            )
            print("Heart rate data saved successfully")
        elif topic == "health/userinput/menstrual_cycle":
            save_menstrual_data(
                db,
                data.get("duration"),
                data.get("condition1")
            )
            print("Menstrual cycle data saved successfully")
        else:
            print(f"Unhandled topic: {topic}")
    except Exception as e:
        print(f"Error saving data: {e}")
    finally:
        db.close()  # 关闭会话，防止连接泄漏
        
# Setup MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("Connecting to MQTT Broker...")
client.connect(broker_address, port, 60)
client.loop_forever()
