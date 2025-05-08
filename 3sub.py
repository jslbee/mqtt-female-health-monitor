import paho.mqtt.client as mqtt
import json
import sqlite3
from datetime import datetime
import os

# MQTT 配置
BROKER_ADDRESS = "broker.hivemq.com"  # 使用公共MQTT代理
BROKER_PORT = 1883

# 数据库配置
DB_PATH = os.path.join(os.path.expanduser('~'), 'Desktop', 'health_data.db')

def init_database():
    """初始化SQLite数据库"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 创建经期数据表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS menstrual_cycle (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time_received TEXT NOT NULL,
                duration REAL NOT NULL,
                condition TEXT NOT NULL
            )
        ''')

        # 创建心率数据表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS heart_rate_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time_received TEXT NOT NULL,
                heart_rate REAL NOT NULL,
                health_status TEXT NOT NULL
            )
        ''')

        # 创建温度数据表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS temperature_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time_received TEXT NOT NULL,
                value REAL NOT NULL,
                warning TEXT,
                trend TEXT
            )
        ''')

        conn.commit()
        print(f"数据库已初始化: {DB_PATH}")
    except Exception as e:
        print(f"数据库初始化错误: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def on_connect(client, userdata, flags, rc):
    """MQTT连接回调"""
    if rc == 0:
        print("成功连接到MQTT代理!")
        client.subscribe("health/userinput/menstrual_cycle", qos=1)  # 经期数据主题
        client.subscribe("health/wearable/heart_rate", qos=1)  # 心率数据主题
        client.subscribe("health/wearable/temperature", qos=1)  # 温度数据主题
    else:
        print(f"连接失败，代码: {rc}")

def on_message(client, userdata, msg):
    """消息接收回调"""
    try:
        data = json.loads(msg.payload.decode())
        time_received = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if msg.topic == "health/userinput/menstrual_cycle":
            print(f"\n接收到经期数据: {data}")
            store_menstrual_data(data['duration'], data['condition'], time_received)

        elif msg.topic == "health/wearable/heart_rate":
            print(f"\n接收到心率数据: {data}")
            store_heart_rate_data(data['heart_rate'], data['health_status'], time_received)
        
        elif msg.topic == "health/wearable/temperature":
            print(f"\n接收到温度数据: {data}")
            store_temperature_data(data['value'], data.get('warning', ''), data.get('trend', ''), time_received)

    except Exception as e:
        print(f"处理消息错误: {e}")

def store_menstrual_data(duration, condition, timestamp):
    """存储经期数据到SQLite"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO menstrual_cycle 
            (time_received, duration, condition)
            VALUES (?, ?, ?)
        ''', (timestamp, duration, condition))
        conn.commit()
        print("经期数据已存储到数据库")
    except sqlite3.Error as e:
        print(f"数据库错误: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def store_heart_rate_data(heart_rate, health_status, timestamp):
    """存储心率数据到SQLite"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO heart_rate_data 
            (time_received, heart_rate, health_status)
            VALUES (?, ?, ?)
        ''', (timestamp, heart_rate, health_status))
        conn.commit()
        print("心率数据已存储到数据库")
    except sqlite3.Error as e:
        print(f"数据库错误: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def store_temperature_data(value, warning, trend, timestamp):
    """存储温度数据到SQLite"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO temperature_data 
            (time_received, value, warning, trend)
            VALUES (?, ?, ?, ?)
        ''', (timestamp, value, warning, trend))
        conn.commit()
        print("温度数据已存储到数据库")
    except sqlite3.Error as e:
        print(f"数据库错误: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    # 初始化数据库
    init_database()
    
    # 设置MQTT客户端
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        client.connect(BROKER_ADDRESS, BROKER_PORT)
        print("等待数据...")
        client.loop_forever()
    except Exception as e:
        print(f"MQTT错误: {e}")
    finally:
        client.disconnect()
