import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime
import sqlite3  # 新增导入


# 数据库初始化函数（保持不变）
def init_db():
    conn = sqlite3.connect('health_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS heart_rate_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time_received TEXT NOT NULL,
            heart_rate REAL,
            health_status TEXT
        )
    ''')
    conn.commit()
    conn.close()


# 配置参数
BROKER_ADDRESS = "test.mosquitto.org"
BROKER_PORT = 1883

# 初始化数据库连接
init_db()

# MQTT客户端设置
client = mqtt.Client()
client.connect(BROKER_ADDRESS, BROKER_PORT)
client.loop_start()

try:
    while True:
        # 生成随机心率数据
        heart_rate = random.uniform(50, 120)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 确定健康状态
        if heart_rate < 60:
            health_status = "偏低"
        elif heart_rate > 100:
            health_status = "偏高"
        else:
            health_status = "正常"

        # 准备MQTT消息
        data = {
            "heart_rate": heart_rate,
            "timestamp": timestamp,
            "health_status": health_status
        }
        payload = json.dumps(data)

        # 发布到MQTT
        result = client.publish("health/wearable/heart_rate", payload, qos=1)
        status = result[0]

        if status == 0:
            print(f"消息已发送 [{timestamp}]: 心率 {heart_rate} BPM，状态 {health_status}")

            # 存储到数据库
            try:
                conn = sqlite3.connect('health_data.db')
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO heart_rate_data 
                    (time_received, heart_rate, health_status)
                    VALUES (?, ?, ?)
                ''', (timestamp, heart_rate, health_status))
                conn.commit()
                print("  数据已存储到数据库")
            except sqlite3.Error as e:
                print(f"  数据库错误: {e}")
            finally:
                if conn:
                    conn.close()
        else:
            print("消息发送失败!")

        time.sleep(5)

except KeyboardInterrupt:
    print("\n程序已终止")
finally:
    client.loop_stop()
    client.disconnect()