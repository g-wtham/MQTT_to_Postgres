import paho.mqtt.client as mqtt

broker = 'broker.emqx.io'
port_no = 1883
topic = 'gowtham/random_data'

def subscriber_model():
    try:
        client = mqtt.Client()
        client.connect(broker, port_no)
        client.subscribe(topic=topic)
        client.on_message = received_message
        client.loop_forever()
    except KeyboardInterrupt:
        client.disconnect()
        print("Client Disconnected")
    
def received_message(client, userData, message):
    print(f"Received Message: {message.payload.decode()} - Topic Subscribed: {topic}")
    
subscriber_model()
