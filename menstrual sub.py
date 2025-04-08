import paho.mqtt.client as mqtt
import json
from datetime import date, datetime
import sqlite3

def determine_health_status(duration,condition,time_received):
    print(f"Duration {duration}, Condition {condition}, Time {time_received}")


def insert_data_into_database(duration, condition, time_received):
    try:
        conn = sqlite3.connect('health_data.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO menstrual_cycle (time_received, duration, condition) VALUES (?, ?, ?)",
                      (time_received, duration, condition))
        conn.commit()
        print("Data inserted into database successfully.")
    except sqlite3.Error as e:
        print("Error inserting data into database:", e)

    finally:
        if conn:
            conn.close()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Subscriber connected successfully to Broker with result code:", rc)
        client.subscribe("health/userinput/menstrual_cycle",qos=1)
    else:
        print("Subscriber connection failed with result code:", rc)

def on_message(client, userdata, msg):
    try:
        #get massage from publisher
        data = json.loads(msg.payload.decode("utf8"))
        duration = data.get('duration', 0)
        condition = data.get('condition', 0)
        time_received = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        determine_health_status(duration,condition,time_received)
        insert_data_into_database(duration,condition, time_received)

    except Exception as e:
        print("Error processing message:", e)


# Main execution
if __name__ == "__main__":

    # Initialize MQTT client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to broker
    try:
        client.connect("120.76.249.191", 1883)
        print("Connecting to broker...")
        client.loop_forever()
    except Exception as e:
        print("Failed to connect to broker:", e)

