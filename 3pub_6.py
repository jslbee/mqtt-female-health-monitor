import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

# MQTT Broker Configuration
BROKER_ADDRESS = "120.76.249.191"  # Public MQTT broker
BROKER_PORT = 1883

# Temperature Threshold Configuration
class TemperatureThresholds:
    """Temperature threshold configuration class"""
    NORMAL_MIN = 36.0  # Normal minimum temperature
    NORMAL_MAX = 37.2  # Normal maximum temperature
    FEVER_LOW = 37.5   # Low fever temperature
    FEVER_HIGH = 38.0  # High fever temperature
    HYPOTHERMIA = 35.5 # Hypothermia warning threshold

# Temperature Data Generator
class TemperatureGenerator:
    """Temperature data generator"""
    def __init__(self):
        self.temp_history = []  # Store recent temperature data
    
    def generate_temperature(self):
        """Generate simulated temperature data"""
        # Generate a random temperature between 35.5-38.5
        temp = round(random.uniform(35.5, 38.5), 1)
        
        # Generate data dictionary 
        temp_data = {
            "value": temp,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Add warning information
        warning = self._check_temperature(temp)
        if warning:
            temp_data["warning"] = warning
        
        # Save to history
        self.temp_history.append(temp)
        if len(self.temp_history) > 10:  # Keep only last 10 records
            self.temp_history.pop(0)
        
        # Analyze trend
        trend = self._analyze_trend()
        if trend:
            temp_data["trend"] = trend
        
        return temp_data
    
    def _check_temperature(self, temp):
        """Check if temperature needs warning"""
        if temp < TemperatureThresholds.HYPOTHERMIA:
            return "Temperature too low, please keep warm"
        elif temp >= TemperatureThresholds.FEVER_HIGH:
            return "High fever warning, medical attention recommended"
        elif temp >= TemperatureThresholds.FEVER_LOW:
            return "Low fever warning, please rest"
        elif temp < TemperatureThresholds.NORMAL_MIN:
            return "Temperature slightly low, keep warm"
        elif temp > TemperatureThresholds.NORMAL_MAX:
            return "Temperature slightly high, please monitor"
        return None
    
    def _analyze_trend(self):
        """Analyze temperature trend"""
        if len(self.temp_history) < 3:
            return None
        
        # Get last three temperature records
        recent_temps = self.temp_history[-3:]
        
        # Calculate average change
        changes = [recent_temps[i] - recent_temps[i-1] for i in range(1, len(recent_temps))]
        avg_change = sum(changes) / len(changes)
        
        if avg_change > 0.2:
            return "Temperature showing upward trend, please monitor closely"
        elif avg_change < -0.2:
            return "Temperature showing downward trend, please keep warm"
        return None

# Generate menstrual condition based on random duration
def check_menstrual_cycle(duration):
    if duration < 5:
        condition = "Caution! You may be so stressed these days!"
    elif 5 <= duration <= 7:
        condition = "Great condition! Keep going girl!"
    else:
        condition = "Caution! Your body may seek for some help!"
    return condition

# Generate health status based on heart rate
def generate_health_status(heart_rate):
    """Generate health status based on heart rate"""
    if heart_rate < 60:
        return "偏低"
    elif heart_rate > 100:
        return "偏高"
    else:
        return "正常"

# Callback function when data is published
def on_publish(client, userdata, mid):
    """Callback function when sending data"""
    print(f"Data published, message ID: {mid}")

# Main publisher function
def publisher():
    client = mqtt.Client()
    client.on_publish = on_publish
    
    # Create instances for temperature, menstrual, and heart rate data generation
    temp_generator = TemperatureGenerator()
    
    client.connect(BROKER_ADDRESS, BROKER_PORT, 60)
    client.loop_start()
    
    try:
        while True:
            # 1. Generate menstrual cycle data
            duration = random.randint(3, 8)
            condition = check_menstrual_cycle(duration)
            menstrual_data = {
                "duration": duration,
                "condition": condition
            }
            menstrual_payload = json.dumps(menstrual_data)
            
            # Publish menstrual data to MQTT topic
            client.publish("health/userinput/menstrual_cycle", menstrual_payload, qos=1)
            print(f"经期数据已发布: {menstrual_payload}")
            
            # 2. Generate heart rate data
            heart_rate = round(random.uniform(50, 120), 2)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            health_status = generate_health_status(heart_rate)
            heart_rate_data = {
                "heart_rate": heart_rate,
                "timestamp": timestamp,
                "health_status": health_status
            }
            heart_rate_payload = json.dumps(heart_rate_data)
            
            # Publish heart rate data to MQTT topic
            client.publish("health/wearable/heart_rate", heart_rate_payload, qos=1)
            print(f"[{timestamp}] 心率数据已发布: {heart_rate_payload}")
            
            # 3. Generate temperature data
            temp_data = temp_generator.generate_temperature()
            temp_payload = json.dumps(temp_data)
            
            # Publish temperature data to MQTT topic
            client.publish("health/wearable/temperature", temp_payload, qos=1)
            print(f"温度数据已发布: {temp_payload}")
            
            # Send data again after 30 seconds
            time.sleep(30)
    
    except KeyboardInterrupt:
        print("\n程序已停止")
        client.loop_stop()
        client.disconnect()
    except Exception as e:
        print(f"发生错误: {e}")
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    publisher()
