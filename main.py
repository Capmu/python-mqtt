import time
import random
import ssl
import paho.mqtt.client as mqtt

# MQTT broker details
broker_address = "<broker-url>"
broker_port = 1883
topic = "<topic-name>"
client_id = f'<client-prefix>-{random.randint(0, 1000)}' #can be anything unique
username = '<mqtt-client-username>'
password = '<mqtt-client-password>'

# Callback triggered when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTTS broker")
        client.connected_flag = True
    else:
        print("Connection failed. RC: ", rc)
        client.bad_connection_flag = True

# Function to publish an MQTT message
def publish_message(client, message):
    result, _ = client.publish(topic, message)
    if result == mqtt.MQTT_ERR_SUCCESS:
        print("Message published successfully")
    else:
        print("Failed to publish message. Error code: ", result)

# Main script
def main():
    client = mqtt.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connected_flag = False
    client.bad_connection_flag = False

    # Configure SSL/TLS
    context = ssl.create_default_context()
    client.tls_set_context(context)

    # Connect to the MQTTS broker
    client.connect(broker_address, broker_port, 60)

    # Loop until the client is connected or the connection fails
    while not client.connected_flag and not client.bad_connection_flag:
        client.loop()
        print('Connecting to the MQTTS broker...')
        time.sleep(1)

    if client.connected_flag:
        # Connection successful, publish the message
        message = "Hello, MQTTS!"
        publish_message(client, message)
    else:
        print("Connection failed. Cannot publish message.")

    # Disconnect from the broker
    client.disconnect()

if __name__ == "__main__":
    main()
