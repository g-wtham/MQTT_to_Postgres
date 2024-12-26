import paho.mqtt.client as mqtt
import psycopg2 as postgres
import datetime

# MQTT broker
broker = 'broker.emqx.io'
port_no = 1883
topic = 'mqtt_db/random_values'

# Database parameters for connecting :
postgres_db = {
    'database' : 'mqtt_db',
    'user' : 'postgres',
    'password' : 'root',
    'host' : '127.0.0.1',
    'port' : '5432'
}

'''
Steps :
1. Receive data from MQTT broker (EMQX).
    i. create client instance of mqtt
    ii. connect to the emqx broker on the corresponding port number
    iii. invoke the callback (on_message), which gets triggered as the message is received.
2. Subscribe to the topic, show the received message along with the timestamp it got received.
3. Update the received values which we got from MQTT to database (postgres in my case), with timestamp
    i. Connect to the postgres db, create cursor object for executing queries from python code.
    ii. Run sql queries using cursor object (using cursor.execute)
    iii. Update values to the db, along with the timestamp. 
4. Find the dif between received timestamp and updated timestamp to know the difference.
'''

def alter_columns(column_name, data_type):
        db_con = postgres.connect(**postgres_db)
        cursor = db_con.cursor()
        cursor.execute(f"ALTER TABLE mqtt_data ADD COLUMN {column_name} {data_type}")
        cursor.close()
        db_con.close()
        
# alter_columns("TIME_DIFFERENCE", "TIMESTAMP")

def on_message(client, userdata, message):
    mqtt_received_time = datetime.datetime.now()
    print(f"Received Message: {message.payload.decode()} for the topic {message.topic} at '{mqtt_received_time}'")
    try:
        db_con = postgres.connect(**postgres_db)
        cursor = db_con.cursor()
        cursor.execute("INSERT into mqtt_data(topic, message) VALUES (%s, %s)", (message.topic, message.payload.decode()))
        db_con.commit()
        print("Message saved to database.")

        
        cursor.execute("SELECT received_time from mqtt_data ORDER BY received_time DESC LIMIT 1")
        received_time_in_db = cursor.fetchone()[0]
        cursor.close()
        db_con.close()
 
        time_df = received_time_in_db - mqtt_received_time
        print("Received Time from MQTT & DB Update Difference: ", time_df, end="\n")
        print("\n")
        
        # cursor.execute("INSERT INTO mqtt_data(TIME_DIFFERENCE TIMESTAMP)")
  
    except Exception as e:
        print(f"Error saving to database: {e}")

client = mqtt.Client()
client.connect(broker, port_no)
client.subscribe(topic)
client.on_message = on_message

print(f"Subscribed to topic: {topic}. Waiting for messages...")

try:
    client.loop_forever()
except KeyboardInterrupt:
    client.disconnect()
    print("Keyboard Interuption")

# Key Note :

# The values sent & received from the database are always in TUPLE, as values can be of multiple columns,
# tuple is used to return from DATABASE and while sending to DB also, it is sent as TUPLE   

# The time difference is in interval format, so updating it should follow interval format



    




