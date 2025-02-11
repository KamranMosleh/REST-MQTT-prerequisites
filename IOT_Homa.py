Question 2 (Intermediate):
Now let's move on to an intermediate example. Write a script that:

Subscribes to the topic home/temperature and prints any message it receives.
The script should publish a message "28°C" to the same topic after 5 seconds of receiving a message.



ANSWER:

import paho.mqtt.client as PahoMQTT
import time

class MySubscriber():
    def __init__(self, clientID, topic, broker):
        self.clientID = clientID
        self.topic = topic
        self.messageBroker = broker
        self._paho_mqtt = PahoMQTT.Client(clientID, True)
        self._paho_mqtt.on_connect = self.myOnConnect
        self._paho_mqtt.on_message = self.myOnMessage

    def start(self):
        self._paho_mqtt.connect(self.messageBroker, 1883)
        self._paho_mqtt.loop_start()
        self._paho_mqtt.subscribe(self.topic, 2)

    def stop(self):
        self._paho_mqtt.unsubscribe(self.topic)
        self._paho_mqtt.loop_stop()
        self._paho_mqtt.disconnect()

    def myOnConnect(self, paho_mqtt, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    def myOnMessage(self, paho_mqtt, userdata, msg):
        print(f"Received message: '{msg.payload.decode()}' on topic '{msg.topic}' with QoS {msg.qos}")

        # Publish a new message after 5 seconds
        time.sleep(5)
        self._paho_mqtt.publish(self.topic, "28°C", 2)
        print("Published message: '28°C'")

if __name__ == '__main__':
    client_id = 'mamad'  # Corrected to a string
    broker = 'mqtt.eclipseprojects.io'
    topic = "home/temperature"

    subscribe = MySubscriber(client_id, topic, broker)
    subscribe.start()

    try:
        while True:
            time.sleep(1)  # Keep the script running to allow message handling
    except KeyboardInterrupt:
        print("Stopping the subscriber...")
        subscribe.stop()

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Problem Statement:
You need to create a temperature sensor class that will:

Simulate Temperature Data:

The sensor should generate a random temperature value between 20°C and 30°C every 10 seconds.
Store Data:

The sensor should store the last 12 temperature readings.
Publish Data:

Every minute, the sensor should publish all the stored data (the last 12 readings) to an MQTT topic in SenML format.
Use of SenML:

SenML (Sensor Markup Language) is a format for representing simple sensor measurements and device parameters. The data should be published in JSON format, using the SenML structure.
MQTT Class Usage:

You should make use of the MyPublisher class we developed earlier for MQTT communication.
Steps to Consider:
Create a Sensor Class:

The class should handle data generation, storage, and MQTT publishing.
Generate Random Temperature:

Use Python’s random module to simulate temperature data.
Store Last 12 Readings:

Maintain a list to keep track of the last 12 temperature readings.
Publish Data Every Minute:

Use time.sleep(10) for the temperature readings and time.sleep(60) for publishing.
SenML Format:

The data should be published in JSON with the SenML format, including fields like "bn" (base name), "bt" (base time), "e" (events), and "v" (value).


import random
import time
import json
from collections import deque
import paho.mqtt.client as mqtt


class TemperatureSensorPublisher:
    def __init__(self, clientID, broker, topic):
        """
        Initializes the TemperatureSensorPublisher class.
        """
        self.clientID = clientID
        self.broker = broker
        self.topic = topic
        self.mqtt_client = mqtt.Client(self.clientID)

        # Register the on_connect callback
        self.mqtt_client.on_connect = self.on_connect

        # Store the last 12 temperature readings
        self.temperature_readings = deque(maxlen=12)
        self.base_name = "temperature_sensor"
        self.base_time = int(time.time())  # Base time for SenML

    def on_connect(self, client, userdata, flags, rc):
        """
        Callback function when the client connects to the broker.
        """
        if rc == 0:
            print("Connected to MQTT broker.")
        else:
            print(f"Failed to connect, return code {rc}")

    def start(self):
        """
        Starts the MQTT client and connects to the broker.
        """
        self.mqtt_client.connect(self.broker, 1883)
        self.mqtt_client.loop_start()

    def stop(self):
        """
        Stops the MQTT client and disconnects.
        """
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()

    def generate_temperature(self):
        """
        Simulates temperature data generation.
        """
        temperature = round(random.uniform(20, 30), 2)  # Random temperature between 20°C and 30°C
        self.temperature_readings.append(temperature)
        print(f"Generated Temperature: {temperature}°C")

    def publish_data(self):
        """
        Publishes the stored data in SenML format.
        """
        # Create the SenML data dictionary
        senml_data = {
            "bn": self.base_name,
            "bt": self.base_time,
            "e": []  # Initialize an empty list for events
        }

        # Populate the "e" field with temperature readings
        for idx, temp in enumerate(self.temperature_readings):
            event = {
                "v": temp,  # Temperature value
                "t": idx * 10  # Time offset relative to base time
            }
            senml_data["e"].append(event)

        # Convert the dictionary to a JSON string
        message = json.dumps(senml_data)

        # Publish the message to the MQTT topic
        self.mqtt_client.publish(self.topic, message, qos=1)
        print(f"Published SenML Data: {message}")


# Main
if __name__ == "__main__":
    # Create an instance of the temperature sensor publisher
    sensor = TemperatureSensorPublisher("temperature_sensor", "mqtt.eclipseprojects.io", "home/sensors/temperature")
    sensor.start()

    last_publish_time = time.time()  # Track the last publish time

    try:
        while True:
            # Generate a new temperature reading
            sensor.generate_temperature()

            # Check if 1 minute has passed for publishing data
            if time.time() - last_publish_time >= 60:
                sensor.publish_data()
                last_publish_time = time.time()  # Reset the timer

            time.sleep(10)  # Wait for the next temperature generation
    except KeyboardInterrupt:
        # Gracefully stop the sensor when interrupted
        sensor.stop()
        print("Sensor stopped.")


++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Question:
Scenario: You are developing an IoT system for a smart home, where various sensors and devices communicate using the MQTT protocol. The system includes temperature sensors, humidity sensors, and lights. Each device publishes data to specific MQTT topics, and a central controller subscribes to these topics to make decisions based on the received data.

Task:
MQTT Topic Structure:

Design a topic structure for the smart home system, considering the following devices:
Temperature sensors located in different rooms (e.g., living room, bedroom).
Humidity sensors located in different rooms.
Lights located in different rooms, which can be turned on/off and dimmed.
MQTT Client Implementation:

Write a Python script using the paho-mqtt library to implement an MQTT client that subscribes to all topics related to lights in the smart home. The client should:
Print the received messages to the console.
Respond to a specific command ("lights/all/set") to turn off all lights when a message with the payload "off" is received.


ANSWER
import paho.mqtt.client as mqtt

# Define the topic structure for your smart home system
TOPIC_TEMPERATURE = "home/+/temperature"
TOPIC_HUMIDITY = "home/+/humidity"
TOPIC_LIGHTS = "home/+/lights"
TOPIC_LIGHTS_ALL_SET = "home/lights/all/set"


class SmartHomeController:
    def __init__(self, clientID, broker):
        """
        Initializes the SmartHomeController.

        Parameters:
        - clientID: Unique identifier for the MQTT client.
        - broker: MQTT broker address.
        """
        self.clientID = clientID
        self.broker = broker
        self.mqtt_client = mqtt.Client(self.clientID)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        """
        Handles connection to the MQTT broker and subscribes to topics.
        """
        if rc == 0:
            print("Connected to broker.")
            # Subscribe to all relevant topics
            self.mqtt_client.subscribe(TOPIC_TEMPERATURE)
            self.mqtt_client.subscribe(TOPIC_HUMIDITY)
            self.mqtt_client.subscribe(TOPIC_LIGHTS)
            self.mqtt_client.subscribe(TOPIC_LIGHTS_ALL_SET)
            print(f"Subscribed to topics: {TOPIC_TEMPERATURE}, {TOPIC_HUMIDITY}, {TOPIC_LIGHTS}, {TOPIC_LIGHTS_ALL_SET}")
        else:
            print(f"Connection failed with code {rc}")

    def on_message(self, client, userdata, msg):
        """
        Handles incoming messages and processes them.
        """
        payload = msg.payload.decode()
        print(f"Message received on {msg.topic}: {payload}")
        if msg.topic == TOPIC_LIGHTS_ALL_SET and payload.lower() == "off":
            print("Command received: Turn off all lights")

    def start(self):
        """
        Starts the MQTT client and connects to the broker.
        """
        self.mqtt_client.connect(self.broker, 1883)
        self.mqtt_client.loop_start()

    def stop(self):
        """
        Stops the MQTT client and disconnects from the broker.
        """
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()


# Example usage
if __name__ == "__main__":
    broker_address = "mqtt.eclipseprojects.io"
    client_id = "smart_home_controller"

    controller = SmartHomeController(client_id, broker_address)
    controller.start()
    try:
        while True:
            pass  # Keep running
    except KeyboardInterrupt:
        controller.stop()
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Question:

You are building an MQTT-based system to monitor and control various devices in a smart building. Each device sends periodic status updates to a specific topic, and the controller subscribes to these topics to take appropriate actions based on the device status.

Task:

Create a class DeviceController that subscribes to a topic based on device type and location.
The controller should print out a custom message when it receives a status update from any device.
Implement a method process_message(self, msg) inside the DeviceController class to handle the message received.
The method should decode the message payload, extract the status (e.g., "ON", "OFF"), and print a message that includes the device type, location, and status.
Use parameters (params) to dynamically change the subscribed topic based on the device type and location.
Example Scenario:

Device: Light
Location: Living Room
Topic: building/smart_home/light/living_room
The controller should subscribe to this topic and, upon receiving a status update (e.g., "ON"), print: "Light in Living Room is ON"

Hints:

Use the on_message callback to trigger the process_message method.
Make use of MQTT parameters to dynamically build the topic for different devices and locations.


ANSWER:
import paho.mqtt.client as mqtt

class DeviceController:
    def __init__(self, clientID, broker, device_type, location):
        """
        Initializes the DeviceController.

        Parameters:
        - clientID: Unique identifier for the MQTT client.
        - broker: MQTT broker address.
        - device_type: Type of the device (e.g., "light", "temperature").
        - location: Location of the device (e.g., "living_room").
        """
        self.clientID = clientID
        self.broker = broker
        self.device_type = device_type
        self.location = location
        self.topic = f"building/smart_home/{device_type}/{location}"

        self.mqtt_client = mqtt.Client(self.clientID)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        """
        Handles connection to the MQTT broker and subscribes to the topic.
        """
        if rc == 0:
            print(f"Connected to broker. Subscribing to {self.topic}")
            self.mqtt_client.subscribe(self.topic)
        else:
            print(f"Connection failed with code {rc}")

    def on_message(self, client, userdata, msg):
        """
        Handles incoming messages and processes them.
        """
        self.process_message(msg)

    def process_message(self, msg):
        """
        Processes the received message by decoding the payload and printing a custom message.
        """
        payload = msg.payload.decode()
        device_name = self.device_type.capitalize()
        location_name = self.location.replace('_', ' ').title()
        print(f"{device_name} in {location_name} is {payload}")

    def start(self):
        """
        Starts the MQTT client and connects to the broker.
        """
        self.mqtt_client.connect(self.broker, 1883)
        self.mqtt_client.loop_start()

    def stop(self):
        """
        Stops the MQTT client and disconnects from the broker.
        """
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()


# Example usage
if __name__ == "__main__":
    device_type = "light"
    location = "living_room"
    clientID = "device_controller_light_livingroom"
    broker = "mqtt.eclipseprojects.io"

    controller = DeviceController(clientID, broker, device_type, location)
    controller.start()
    try:
        while True:
            pass  # Keep running
    except KeyboardInterrupt:
        controller.stop()
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Scenario:

You are tasked with developing a monitoring system for a smart greenhouse. The system will have multiple sensors (e.g., temperature, humidity, soil moisture) that publish data to different MQTT topics. You need to design a Python class that can subscribe to these topics, collect the sensor data, and calculate the average values over a 5-minute window. The results should be published to a summary topic every 5 minutes.

Requirements:

Subscription to Multiple Topics:

The class should subscribe to three MQTT topics: "greenhouse/temperature", "greenhouse/humidity", and "greenhouse/soil_moisture".
Data Collection and Averaging:

The class should store the incoming sensor data and calculate the average values for each sensor over the last 5 minutes.
The data should be stored in a list for each sensor, with each entry containing the sensor reading and the timestamp.
Periodic Publishing:

Every 5 minutes, the class should calculate the average values for the temperature, humidity, and soil moisture sensors and publish the results to the topic "greenhouse/summary" in JSON format.
MQTT Implementation:

Implement the MQTT client using the paho-mqtt library.
Ensure the MQTT client handles reconnections in case of a connection loss.
Questions:

How would you structure the class to handle subscriptions to multiple topics?
What data structures would you use to store the sensor data for averaging?
How would you ensure the class calculates the averages and publishes them exactly every 5 minutes?
How would you handle MQTT connection issues, such as disconnects or timeouts?
Bonus:

Can you add a feature to detect anomalies (e.g., temperature above 40°C) and immediately publish an alert to a topic "greenhouse/alerts"?




ANSWER:


import paho.mqtt.client as mqtt
import time
import json


class SmartGreenhouse:
    def __init__(self, clientID, broker):
        """
        Initializes the SmartGreenhouse class.
        """
        self.clientID = clientID
        self.broker = broker
        self.mqtt_client = mqtt.Client(self.clientID)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message

        self.data = {
            "greenhouse/temperature": [],
            "greenhouse/humidity": [],
            "greenhouse/soil_moisture": []
        }
        self.start_time = time.time()

    def on_connect(self, client, userdata, flags, rc):
        """
        Handles connection to the MQTT broker and subscribes to sensor topics.
        """
        if rc == 0:
            print("Connected to broker.")
            for topic in self.data.keys():  # Subscribe to all topics in self.data
                self.mqtt_client.subscribe(topic)
                print(f"Subscribed to: {topic}")
        else:
            print(f"Connection failed: {rc}")

    def on_message(self, client, userdata, msg):
        """
        Handles incoming sensor data and stores it.
        """
        topic = msg.topic
        reading = float(msg.payload.decode())  # Convert payload to float
        self.data[topic].append(reading)
        print(f"{topic} -> {reading}")

        # Check for anomaly (temperature > 40)
        if topic == "greenhouse/temperature" and reading > 40:
            self.mqtt_client.publish(
                "greenhouse/alerts",
                json.dumps({"sensor": "temperature", "value": reading, "message": "Anomaly detected"})
            )
            print(f"Published alert for {topic}: {reading}")

        # Publish summary every 5 minutes
        if time.time() - self.start_time >= 300:
            self.publish_summary()

    def publish_summary(self):
        """
        Calculates averages for each sensor and publishes the summary.
        """
        summary = {}
        for topic, readings in self.data.items():
            if readings:  # Only calculate if there are readings
                sensor_type = topic.split("/")[-1]  # Extract sensor type
                avg_value = sum(readings) / len(readings)  # Calculate average
                summary[sensor_type] = avg_value
                self.data[topic] = []  # Clear data for the topic
        self.mqtt_client.publish("greenhouse/summary", json.dumps(summary))  # Publish the summary
        self.start_time = time.time()  # Reset the timer
        print(f"Published summary: {summary}")

    def start(self):
        """
        Starts the MQTT client and connects to the broker.
        """
        self.mqtt_client.connect(self.broker, 1883)
        self.mqtt_client.loop_start()

    def stop(self):
        """
        Stops the MQTT client and disconnects from the broker.
        """
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()
        print("Disconnected from broker.")


# Example usage
if __name__ == "__main__":
    greenhouse = SmartGreenhouse("greenhouse_monitor", "mqtt.eclipseprojects.io")
    greenhouse.start()

    try:
        while True:
            time.sleep(1)  # Keep running
    except KeyboardInterrupt:
        greenhouse.stop()

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Question: Temperature and Humidity Monitoring System
You are tasked with creating a temperature and humidity monitoring system using MQTT. The system must satisfy the following requirements:

Data Collection:

A sensor generates random temperature and humidity values every 15 seconds.
The temperature should be between -10°C and 50°C.
The humidity should be between 0% and 100%.
Data Storage:

The system should store the last 20 readings for both temperature and humidity.
Data Analysis:

Every 2 minutes, the system should calculate the average temperature and humidity.
If the average temperature exceeds 30°C or the average humidity exceeds 70%, it should trigger an alert by publishing a message to the "alerts" topic.
Data Publishing:

Every 2 minutes, the system should publish the average temperature and humidity values to the "monitoring/temperature" and "monitoring/humidity" topics in JSON format.
MQTT Configuration:

Use mqtt.eclipseprojects.io as the broker.
Use QoS level 1 for publishing and subscribing.
Tasks:
Implement the MQTT client class that handles all the above functionalities.
Ensure the program runs indefinitely, collecting, analyzing, and publishing data as described.
The output should include messages for when alerts are triggered.

ANSWER:

import paho.mqtt.client as mqtt
import random
import time
import json
from collections import deque

# Global topic definitions
TEMP_TOPIC = "monitoring/temperature"
HUMIDITY_TOPIC = "monitoring/humidity"
ALERTS_TOPIC = "alerts"

class MonitoringSystem:
    def __init__(self, clientID, broker):
        """
        Initializes the MonitoringSystem class.
        """
        self.clientID = clientID
        self.broker = broker
        self.mqtt_client = mqtt.Client(self.clientID)
        self.mqtt_client.on_connect = self.on_connect

        # Store the last 20 readings using deque
        self.temperature_readings = deque(maxlen=20)
        self.humidity_readings = deque(maxlen=20)

    def on_connect(self, client, userdata, flags, rc):
        """
        Handles connection to the MQTT broker.
        """
        if rc == 0:
            print("Connected to broker.")
        else:
            print(f"Connection failed with code {rc}")

    def generate_readings(self):
        """
        Simulates sensor data generation every 15 seconds.
        """
        temperature = round(random.uniform(-10, 50), 2)  # Generate random temperature
        humidity = round(random.uniform(0, 100), 2)  # Generate random humidity
        self.temperature_readings.append(temperature)
        self.humidity_readings.append(humidity)
        print(f"Generated readings: Temperature={temperature}°C, Humidity={humidity}%")

    def calculate_averages_and_publish(self):
        """
        Calculates averages, publishes to MQTT topics, and triggers alerts if necessary.
        """
        # Check if there are readings before calculating averages
        if len(self.temperature_readings) > 0 and len(self.humidity_readings) > 0:
            avg_temp = sum(self.temperature_readings) / len(self.temperature_readings)
            avg_humidity = sum(self.humidity_readings) / len(self.humidity_readings)

            # Publish averages
            self.mqtt_client.publish(TEMP_TOPIC, json.dumps({"average_temperature": avg_temp}), qos=1)
            self.mqtt_client.publish(HUMIDITY_TOPIC, json.dumps({"average_humidity": avg_humidity}), qos=1)
            print(f"Published: Average Temperature={avg_temp}°C, Average Humidity={avg_humidity}%")

            # Trigger alerts for temperature
            if avg_temp > 30:
                temp_alert = {
                    "sensor": "temperature",
                    "value": avg_temp,
                    "alert": "High Temperature"
                }
                self.mqtt_client.publish(ALERTS_TOPIC, json.dumps(temp_alert), qos=1)
                print(f"Temperature alert published: {temp_alert}")

            # Trigger alerts for humidity
            if avg_humidity > 70:
                humidity_alert = {
                    "sensor": "humidity",
                    "value": avg_humidity,
                    "alert": "High Humidity"
                }
                self.mqtt_client.publish(ALERTS_TOPIC, json.dumps(humidity_alert), qos=1)
                print(f"Humidity alert published: {humidity_alert}")
        else:
            print("Not enough data to calculate averages.")

    def start(self):
        """
        Starts the MQTT client and connects to the broker.
        """
        self.mqtt_client.connect(self.broker, 1883)
        self.mqtt_client.loop_start()

    def stop(self):
        """
        Stops the MQTT client and disconnects.
        """
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()
        print("Disconnected from broker.")


# Main
if __name__ == "__main__":
    monitoring_system = MonitoringSystem("temp_humidity_monitor", "mqtt.eclipseprojects.io")
    monitoring_system.start()

    last_time = time.time()  # Initialize timer

    try:
    while True:
        monitoring_system.generate_readings()  # Generate new readings first
        if time.time() - last_time >= 120:  # Check if 2 minutes have passed
            monitoring_system.calculate_averages_and_publish()  # Calculate averages and publish
            last_time = time.time()  # Reset the timer
        time.sleep(15)  # Wait for the next reading
except KeyboardInterrupt:
    monitoring_system.stop()

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
New Question:
Scenario: You are developing a smart home system that controls and monitors various devices like lights, fans, and door locks. You need to create a class SmartHomeController that manages the following tasks:

Data Collection:

Simulate data collection from sensors every 30 seconds. The data could be the state of a light (on or off), the state of a fan (on or off), and the status of the door (locked or unlocked).
Store the last 10 states of each device.
Data Publishing:

Every minute, publish the last two collected states of each device to their respective MQTT topics in a JSON format.
Alerts:

If a door is found to be "unlocked" for more than 1 minute (i.e., two consecutive states are "unlocked"), publish an alert message.
Control Commands:

Allow the system to subscribe to a "commands" topic, where it can receive control commands for the devices (e.g., "turn_on_light", "lock_door").
Upon receiving a command, update the device state accordingly and publish the new state to its corresponding topic.
Tasks:
Implement the SmartHomeController class with the following methods:

collect_data: Collect sensor states every 30 seconds.
publish_data: Publish the last two states every minute.
process_alerts: Check and publish alerts based on the device states.
handle_command: Handle incoming commands and update the device states.
start and stop methods for starting and stopping the MQTT client.
Run the system in a loop that continuously collects data, publishes it, and processes any commands received.

ANSWER:
import paho.mqtt.client as mqtt
import time
import json
from collections import deque
import random


class SmartHomeController:
    def __init__(self, clientID, broker):
        """
        Initializes the SmartHomeController class.
        """
        self.clientID = clientID
        self.broker = broker
        self.mqtt_client = mqtt.Client(self.clientID)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.handle_command

        # Device states (store the last 10 states)
        self.light_states = deque(maxlen=10)
        self.fan_states = deque(maxlen=10)
        self.door_states = deque(maxlen=10)

        # MQTT Topics
        self.light_topic = "home/lights"
        self.fan_topic = "home/fans"
        self.door_topic = "home/doors"
        self.commands_topic = "home/commands"
        self.alerts_topic = "home/alerts"

    def on_connect(self, client, userdata, flags, rc):
        """
        Handles connection to the MQTT broker and subscribes to the commands topic.
        """
        if rc == 0:
            print("Connected to broker.")
            self.mqtt_client.subscribe(self.commands_topic)
        else:
            print(f"Connection failed with code {rc}")

    def generate_data(self):
        """
        Simulates generating data from devices every 30 seconds.
        """
        light_state = random.choice(["on", "off"])
        fan_state = random.choice(["on", "off"])
        door_state = random.choice(["locked", "unlocked"])

        self.light_states.append(light_state)
        self.fan_states.append(fan_state)
        self.door_states.append(door_state)

        print(f"Generated states - Light: {light_state}, Fan: {fan_state}, Door: {door_state}")

    def publish_data(self):
        """
        Publishes the last two states of each device every minute.
        """
        data = {
            "light_states": list(self.light_states)[-2:],
            "fan_states": list(self.fan_states)[-2:],
            "door_states": list(self.door_states)[-2:]
        }
        self.mqtt_client.publish(self.light_topic, json.dumps({"light": data["light_states"]}), qos=1)
        self.mqtt_client.publish(self.fan_topic, json.dumps({"fan": data["fan_states"]}), qos=1)
        self.mqtt_client.publish(self.door_topic, json.dumps({"door": data["door_states"]}), qos=1)
        print(f"Published device states: {data}")

    def process_alerts(self):
        """
        Checks for alerts and publishes them if necessary.
        """
        if len(self.door_states) >= 2 and self.door_states[-1] == "unlocked" and self.door_states[-2] == "unlocked":
            alert_message = {"alert": "Door has been unlocked for more than 1 minute!"}
            self.mqtt_client.publish(self.alerts_topic, json.dumps(alert_message), qos=1)
            print(f"Alert published: {alert_message}")

    def handle_command(self, client, userdata, msg):
        """
        Handles incoming commands and updates device states.
        """
        command = msg.payload.decode()
        print(f"Received command: {command}")

        if command == "turn_on_light":
            self.light_states.append("on")
            self.mqtt_client.publish(self.light_topic, json.dumps({"light": "on"}), qos=1)
        elif command == "turn_off_light":
            self.light_states.append("off")
            self.mqtt_client.publish(self.light_topic, json.dumps({"light": "off"}), qos=1)
        elif command == "turn_on_fan":
            self.fan_states.append("on")
            self.mqtt_client.publish(self.fan_topic, json.dumps({"fan": "on"}), qos=1)
        elif command == "turn_off_fan":
            self.fan_states.append("off")
            self.mqtt_client.publish(self.fan_topic, json.dumps({"fan": "off"}), qos=1)
        elif command == "lock_door":
            self.door_states.append("locked")
            self.mqtt_client.publish(self.door_topic, json.dumps({"door": "locked"}), qos=1)
        elif command == "unlock_door":
            self.door_states.append("unlocked")
            self.mqtt_client.publish(self.door_topic, json.dumps({"door": "unlocked"}), qos=1)

    def start(self):
        """
        Starts the MQTT client and connects to the broker.
        """
        self.mqtt_client.connect(self.broker, 1883)
        self.mqtt_client.loop_start()

    def stop(self):
        """
        Stops the MQTT client and disconnects.
        """
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()
        print("Disconnected from broker.")


# Main
if __name__ == "__main__":
    controller = SmartHomeController("smart_home_controller", "mqtt.eclipseprojects.io")
    controller.start()

    last_publish_time = time.time()

    try:
        while True:
            controller.generate_data()  # Generate new data first
            if time.time() - last_publish_time >= 60:  # Check if 1 minute has passed
                controller.publish_data()
                controller.process_alerts()
                last_publish_time = time.time()  # Reset the timer
            time.sleep(30)  # Wait 30 seconds for the next data generation
    except KeyboardInterrupt:
        controller.stop()


