import paho.mqtt.client as mqtt
import json
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import sys

# MQTT 配置
BROKER_ADDRESS = "broker.emqx.io"  # 使用公共MQTT代理
BROKER_PORT = 1883

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',  # 数据库主机
    'user': 'root',      # 数据库用户名
    'password': 'zaq13910975598',  # 数据库密码
    'database': 'health_data'  # 数据库名称
}

def on_connect(client, userdata, flags, rc):
    """MQTT连接回调"""
    if rc == 0:
        print("\n=== MQTT连接成功 ===")
        print("正在订阅主题...")
        # 使用qos=1确保消息可靠传递
        topics = [
            ("health/userinput/menstrual_cycle", 1),
            ("health/wearable/heart_rate", 1),
            ("health/wearable/temperature", 1)
        ]
        client.subscribe(topics)
        print("主题订阅完成")
    else:
        print(f"连接失败，代码: {rc}")

def on_subscribe(client, userdata, mid, granted_qos):
    """订阅回调"""
    print(f"成功订阅主题，消息ID: {mid}, QoS: {granted_qos}")

def on_message(client, userdata, msg):
    """消息接收回调"""
    try:
        print(f"\n=== 收到新消息 ===")
        print(f"主题: {msg.topic}")
        print(f"QoS: {msg.qos}")
        print(f"消息ID: {msg.mid}")
        print(f"原始消息: {msg.payload.decode()}")
        
        data = json.loads(msg.payload.decode())
        time_received = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if msg.topic == "health/userinput/menstrual_cycle":
            print(f"接收到经期数据: {data}")
            print(f"数据格式验证:")
            print(f"- duration存在: {'duration' in data}")
            print(f"- condition存在: {'condition' in data}")
            
            if all(key in data for key in ['duration', 'condition']):
                try:
                    # 确保数据类型正确
                    duration = float(data['duration'])
                    condition = str(data['condition'])
                    print(f"准备存储经期数据:")
                    print(f"- 持续时间: {duration}")
                    print(f"- 状态: {condition}")
                    print(f"- 时间戳: {time_received}")
                    store_menstrual_data(duration, condition, time_received)
                except ValueError as e:
                    print(f"数据类型转换错误: {e}")
            else:
                print("经期数据格式不完整，无法存储")
                print(f"收到的数据: {data}")

        elif msg.topic == "health/wearable/heart_rate":
            print(f"接收到心率数据: {data}")
            print(f"数据格式验证:")
            print(f"- heart_rate存在: {'heart_rate' in data}")
            print(f"- health_status存在: {'health_status' in data}")
            print(f"- timestamp存在: {'timestamp' in data}")
            
            if all(key in data for key in ['heart_rate', 'health_status', 'timestamp']):
                try:
                    # 确保数据类型正确
                    heart_rate = float(data['heart_rate'])
                    health_status = str(data['health_status'])
                    timestamp = str(data['timestamp'])
                    print(f"准备存储心率数据:")
                    print(f"- 心率值: {heart_rate}")
                    print(f"- 健康状态: {health_status}")
                    print(f"- 时间戳: {timestamp}")
                    store_heart_rate_data(heart_rate, health_status, timestamp)
                except ValueError as e:
                    print(f"数据类型转换错误: {e}")
            else:
                print("心率数据格式不完整，无法存储")
                print(f"收到的数据: {data}")
        
        elif msg.topic == "health/wearable/temperature":
            print(f"接收到温度数据: {data}")
            store_temperature_data(data['value'], data.get('warning', ''), data.get('trend', ''), time_received)

    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        print(f"原始消息内容: {msg.payload.decode()}")
    except Exception as e:
        print(f"处理消息错误: {e}")
        print(f"错误类型: {type(e)}")
        print(f"错误详情: {str(e)}")

def store_menstrual_data(duration, condition, timestamp):
    """存储经期数据到MySQL"""
    conn = None
    try:
        print(f"\n=== 开始存储经期数据 ===")
        print(f"数据库配置: {DB_CONFIG}")
        print(f"尝试连接数据库...")
        
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # 检查数据库连接
        cursor.execute("SELECT DATABASE()")
        current_db = cursor.fetchone()[0]
        print(f"当前数据库: {current_db}")
        
        # 检查表是否存在
        cursor.execute("SHOW TABLES LIKE 'menstrual_cycle'")
        table_exists = cursor.fetchone()
        print(f"menstrual_cycle表是否存在: {bool(table_exists)}")
        
        if not table_exists:
            print("创建menstrual_cycle表...")
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS menstrual_cycle (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    time_received DATETIME NOT NULL,
                    duration FLOAT NOT NULL,
                    condition1 VARCHAR(255) NOT NULL
                )
            ''')
            conn.commit()
            print("表创建成功")
        
        # 准备插入数据
        print(f"准备插入数据: 持续时间={duration}, 状态={condition}, 时间={timestamp}")
        
        # 插入数据
        insert_query = '''
            INSERT INTO menstrual_cycle 
            (time_received, duration, condition1)
            VALUES (%s, %s, %s)
        '''
        print(f"执行SQL: {insert_query}")
        print(f"参数: {timestamp}, {duration}, {condition}")
        
        cursor.execute(insert_query, (timestamp, duration, condition))
        conn.commit()
        
        # 验证数据是否插入成功
        cursor.execute("SELECT COUNT(*) FROM menstrual_cycle")
        count = cursor.fetchone()[0]
        print(f"当前表中的记录数: {count}")
        
        # 查询最新插入的数据
        cursor.execute('''
            SELECT * FROM menstrual_cycle 
            ORDER BY id DESC LIMIT 1
        ''')
        latest_record = cursor.fetchone()
        print(f"最新插入的记录: {latest_record}")
        
        print("经期数据已成功存储到数据库")
        
    except Error as e:
        print(f"数据库错误: {e}")
        print(f"错误类型: {type(e)}")
        print(f"错误详情: {str(e)}")
    except Exception as e:
        print(f"存储经期数据时发生错误: {e}")
        print(f"错误类型: {type(e)}")
        print(f"错误详情: {str(e)}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            print("数据库连接已关闭")

def init_database():
    """初始化数据库和表"""
    try:
        print("\n=== 初始化数据库 ===")
        # 首先创建数据库连接（不指定数据库）
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        
        # 创建数据库
        print("创建数据库...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cursor.execute(f"USE {DB_CONFIG['database']}")
        
        # 创建心率数据表
        print("创建心率数据表...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS heart_rate_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                time_received DATETIME NOT NULL,
                heart_rate FLOAT NOT NULL,
                health_status VARCHAR(255) NOT NULL
            )
        ''')
        
        # 创建经期数据表
        print("创建经期数据表...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS menstrual_cycle (
                id INT AUTO_INCREMENT PRIMARY KEY,
                time_received DATETIME NOT NULL,
                duration FLOAT NOT NULL,
                condition1 VARCHAR(255) NOT NULL
            )
        ''')
        
        # 创建温度数据表
        print("创建温度数据表...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS temperature_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                time_received DATETIME NOT NULL,
                value FLOAT NOT NULL,
                warning VARCHAR(255),
                trend VARCHAR(255)
            )
        ''')
        
        conn.commit()
        print("数据库初始化完成")
        
    except Error as e:
        print(f"数据库初始化错误: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def store_heart_rate_data(heart_rate, health_status, timestamp):
    """存储心率数据到MySQL"""
    conn = None
    try:
        print(f"\n=== 开始存储心率数据 ===")
        print(f"数据库配置: {DB_CONFIG}")
        print(f"尝试连接数据库...")
        
        # 尝试连接数据库
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database']
        )
        
        if not conn.is_connected():
            raise Exception("数据库连接失败")
            
        print("数据库连接成功")
        cursor = conn.cursor()
        
        # 检查数据库连接
        cursor.execute("SELECT DATABASE()")
        current_db = cursor.fetchone()[0]
        print(f"当前数据库: {current_db}")
        
        # 检查表是否存在
        cursor.execute("SHOW TABLES LIKE 'heart_rate_data'")
        table_exists = cursor.fetchone()
        print(f"heart_rate_data表是否存在: {bool(table_exists)}")
        
        if not table_exists:
            print("创建heart_rate_data表...")
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS heart_rate_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    time_received DATETIME NOT NULL,
                    heart_rate FLOAT NOT NULL,
                    health_status VARCHAR(255) NOT NULL
                )
            ''')
            conn.commit()
            print("表创建成功")
        
        # 准备插入数据
        print(f"准备插入数据: 心率={heart_rate}, 状态={health_status}, 时间={timestamp}")
        
        # 插入数据
        insert_query = '''
            INSERT INTO heart_rate_data 
            (time_received, heart_rate, health_status)
            VALUES (%s, %s, %s)
        '''
        print(f"执行SQL: {insert_query}")
        print(f"参数: {timestamp}, {heart_rate}, {health_status}")
        
        cursor.execute(insert_query, (timestamp, heart_rate, health_status))
        conn.commit()
        
        # 验证数据是否插入成功
        cursor.execute("SELECT COUNT(*) FROM heart_rate_data")
        count = cursor.fetchone()[0]
        print(f"当前表中的记录数: {count}")
        
        # 查询最新插入的数据
        cursor.execute('''
            SELECT * FROM heart_rate_data 
            ORDER BY id DESC LIMIT 1
        ''')
        latest_record = cursor.fetchone()
        print(f"最新插入的记录: {latest_record}")
        
        print("心率数据已成功存储到数据库")
        
    except Error as e:
        print(f"数据库错误: {e}")
        print(f"错误类型: {type(e)}")
        print(f"错误详情: {str(e)}")
    except Exception as e:
        print(f"存储心率数据时发生错误: {e}")
        print(f"错误类型: {type(e)}")
        print(f"错误详情: {str(e)}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            print("数据库连接已关闭")

def store_temperature_data(value, warning, trend, timestamp):
    """存储温度数据到MySQL"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO temperature_data 
            (time_received, value, warning, trend)
            VALUES (%s, %s, %s, %s)
        ''', (timestamp, value, warning, trend))
        conn.commit()
        print("温度数据已存储到数据库")
    except Error as e:
        print(f"数据库错误: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def query_recent_data():
    """查询最近的数据记录"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # 查询经期数据
        print("\n=== 最近5条经期数据 ===")
        cursor.execute('''
            SELECT * FROM menstrual_cycle 
            ORDER BY time_received DESC 
            LIMIT 5
        ''')
        menstrual_data = cursor.fetchall()
        for row in menstrual_data:
            print(f"时间: {row['time_received']}, 持续时间: {row['duration']}, 状态: {row['condition1']}")
        
        # 查询心率数据
        print("\n=== 最近5条心率数据 ===")
        cursor.execute('''
            SELECT * FROM heart_rate_data 
            ORDER BY time_received DESC 
            LIMIT 5
        ''')
        heart_rate_data = cursor.fetchall()
        for row in heart_rate_data:
            print(f"时间: {row['time_received']}, 心率: {row['heart_rate']}, 健康状态: {row['health_status']}")
        
        # 查询温度数据
        print("\n=== 最近5条温度数据 ===")
        cursor.execute('''
            SELECT * FROM temperature_data 
            ORDER BY time_received DESC 
            LIMIT 5
        ''')
        temperature_data = cursor.fetchall()
        for row in temperature_data:
            print(f"时间: {row['time_received']}, 温度: {row['value']}, 警告: {row['warning']}, 趋势: {row['trend']}")
            
    except Error as e:
        print(f"数据库错误: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--query":
        # 如果命令行参数包含 --query，则执行查询
        query_recent_data()
    else:
        # 初始化数据库
        init_database()
        
        # 设置MQTT客户端
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_subscribe = on_subscribe
        
        try:
            print("正在连接到MQTT代理...")
            print(f"代理地址: {BROKER_ADDRESS}")
            print(f"代理端口: {BROKER_PORT}")
            client.connect(BROKER_ADDRESS, BROKER_PORT, 60)
            print("等待数据...")
            client.loop_forever()
        except Exception as e:
            print(f"MQTT错误: {e}")
            print(f"错误类型: {type(e)}")
            print(f"错误详情: {str(e)}")
        finally:
            client.disconnect()
