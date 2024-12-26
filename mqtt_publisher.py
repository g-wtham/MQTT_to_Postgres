'''
Steps:
1. Import paho-mqtt and create an instance of the MQTT client
2. Assign the port, topic to send data to.
3. Establish connection with the broker (broker.emqx.io) on port 1883, which is used for communication
4. Generate random data and send until a specified loop limit
'''

import paho.mqtt.client as mqtt
import random
import time

broker = 'broker.emqx.io'
port_no = 1883
topic = 'mqtt_db/random_values'

def publish_message():
    client = mqtt.Client()
    client.connect(broker, port_no)
    print("Connected to broker.")

    i = 0
    while (i<10): # Sends message 10 times
        random_data = random.uniform(20, 40)
        message = f"Random Data {i+1} : {random_data:.2f}"
        client.publish(topic=topic, payload=message)
        print(f"Message No. {i+1} Published ")
        time.sleep(5)
        i += 1
    
    print(f"All {i} are sent.")

publish_message()
