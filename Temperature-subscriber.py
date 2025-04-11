import paho.mqtt.client as mqtt 
import json
import pymysql
from datetime import datetime

# MQTT Server Configuration
BROKER = "112.74.107.115"
PORT = 1883
TOPIC_TEMP = "health/wearable/temperature"

# MySQL Database Configuration
DB_HOST = 'localhost'
DB_USER = 'your_username'
DB_PASSWORD = 'your_password'
DB_NAME = 'sql_tutorial1'

# Create database connection
def create_db_connection():
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME)
    return conn

# Create table (if not exists)
def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS temperature_sensor (
                temperatureSensor_ID INT AUTO_INCREMENT PRIMARY KEY,
                user_ID INT NOT NULL,
                temperature DECIMAL(5, 2) NOT NULL,
                record_time DATETIME NOT NULL,
                FOREIGN KEY (user_ID) REFERENCES user(user_ID)
            )
        ''')
        conn.commit()
        print("Table 'temperature_sensor' created successfully")
    except pymysql.Error as e:
        print(f"Error creating table: {e}")
        conn.rollback()

# Insert data
def insert_data(conn, user_id, temperature, timestamp):
    try:
        cursor = conn.cursor()
        cursor.execute(f'''
            INSERT INTO temperature_sensor (user_ID, temperature, record_time)
            VALUES (%s, %s, %s)
        ''', (user_id, temperature, timestamp))
        conn.commit()
        print("Data inserted successfully")
    except pymysql.Error as e:
        print(f"Error inserting data: {e}")
        conn.rollback()

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    """Callback function when connecting to MQTT server"""
    if rc == 0:
        print("Successfully connected to MQTT server")
        client.subscribe(TOPIC_TEMP)
        print(f"Subscribed to topic: {TOPIC_TEMP}")
    else:
        print(f"Connection failed with code: {rc}")

def on_message(client, userdata, msg):
    """Handle received MQTT temperature data"""
    try:
        data = json.loads(msg.payload.decode())
        
        print(f"\nReceived temperature data:")
        print(f"Temperature: {data['value']}°C")
        print(f"Timestamp: {data['timestamp']}")
        
        # Extract user ID
        user_id = data.get('user_id', 1)  # Default to 1 if user_id is not provided
        
        # Insert data into database
        timestamp = datetime.fromisoformat(data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        conn = create_db_connection()
        if conn:
            create_table(conn)
            insert_data(conn, user_id, data['value'], timestamp)
            conn.close()
        else:
            print("Error! Cannot create the database connection.")
        
        if "warning" in data:
            print(f"Warning: {data['warning']}")
        if "trend" in data:
            print(f"Trend: {data['trend']}")
    
    except Exception as e:
        print(f"Error processing message: {e}")

def subscriber():
    """Main subscriber function"""
    conn = create_db_connection()
    if conn:
        create_table(conn)
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        
        try:
            print("Connecting to MQTT server...")
            client.connect(BROKER, PORT, 60)
            client.loop_forever()
        
        except KeyboardInterrupt:
            print("\nProgram stopped")
            client.disconnect()
        except Exception as e:
            print(f"Error occurred: {e}")
            client.disconnect()
    else:
        print("Error! Cannot create the database connection.")

if __name__ == "__main__":
    subscriber()
