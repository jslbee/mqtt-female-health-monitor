import paho.mqtt.client as mqtt 
import json
import time
import random
from datetime import datetime

# MQTT Server Configuration
BROKER_ADDRESS = 120.76.249.191""
BROKER_PORT = 1883
TOPIC_TEMP = "health/wearable/temperature"

# Temperature Threshold Configuration
class TemperatureThresholds:
    """Temperature threshold configuration class"""
    NORMAL_MIN = 36.0  # Normal minimum temperature
    NORMAL_MAX = 37.2  # Normal maximum temperature
    FEVER_LOW = 37.5   # Low fever temperature
    FEVER_HIGH = 38.0  # High fever temperature
    HYPOTHERMIA = 35.5 # Hypothermia warning threshold

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

def on_publish(client, userdata, mid):
    """Callback function when sending data"""
    print(f"Data published, message ID: {mid}")

def publisher():
    """Temperature data publisher"""
    client = mqtt.Client()
    client.on_publish = on_publish
    temp_generator = TemperatureGenerator()
    
    client.connect(BROKER_ADDRESS, BROKER_PORT, 60)
    client.loop_start()
    
    try:
        while True:
            # Generate temperature data
            temp_data = temp_generator.generate_temperature()
            
            # Publish data to MQTT server
            payload = json.dumps(temp_data)
            result = client.publish(TOPIC_TEMP, payload)
            status = result[0]
            
            if status == 0:
                print(f"Message sent at {temp_data['timestamp']}: {payload}")
            else:
                print("Failed to send message!")
            
            # Send data again after 30 seconds
            time.sleep(30)
    
    except KeyboardInterrupt:
        print("\nProgram stopped")
        client.loop_stop()
        client.disconnect()
    except Exception as e:
        print(f"Error occurred: {e}")
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    publisher()

    
   
     


            
