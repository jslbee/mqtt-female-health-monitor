import paho.mqtt.client as mqtt  # 导入MQTT客户端库
import json  # 导入JSON处理库
import time  # 导入时间库
import random  # 导入随机数库

# MQTT代理服务器配置
BROKER_ADDRESS = "broker.hivemq.com"  # 公共测试MQTT服务器地址
BROKER_PORT = 1883  # 默认MQTT端口(非加密)

# 创建客户端实例
client = mqtt.Client()  # 初始化MQTT客户端

# 可选的身份验证设置(根据实际需要配置)
client.username_pw_set("第三组", "password")  # 设置用户名和密码

# 连接到代理服务器
client.connect(BROKER_ADDRESS, BROKER_PORT)  # 建立连接
client.loop_start()  # 启动网络循环(后台线程)

# 循环发布消息
try:
    while True:
        # 构造示例消息(模拟传感器数据)
        # 这里生成随机温度值(60-140之间)
        data = {
            # "tid": "S1",  # 可选的设备ID字段(当前注释掉了)
            "temp": random.uniform(60, 140)  # 生成随机温度值
        }

        # 将字典转换为JSON字符串
        payload = json.dumps(data)  # 序列化为JSON格式

        # 发布到主题 health_monitor/{divice_id}/heart_rate
        # 注意: 主题中的"divice_id"可能是拼写错误，应为"device_id"
        client.publish("health_monitor/{divice_id}/heart_rate", payload)

        print("\n传感器已发布:", payload)  # 控制台输出确认信息

        # 再次发布前等待5秒
        time.sleep(5)  # 5秒间隔

except KeyboardInterrupt:
    # 当程序被键盘中断(Ctrl+C)时优雅退出
    pass
finally:
    # 确保无论如何都执行清理工作
    client.loop_stop()  # 停止网络循环
    client.disconnect()  # 断开与服务器的连接