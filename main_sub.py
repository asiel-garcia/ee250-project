import paho.mqtt.client as mqtt
import json
import matplotlib.pyplot as plt
import time

broker_addy = "172.20.10.10"
broker_port = 1883
username = "asielgar"
pwd = "12345"
topic = "Shower time"
counter = 0
humidities = []
seconds = []
max_humidity=0
is_showering=False

client = mqtt.Client()
client.username_pw_set(username, pwd)

start_time=time.time()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic)

def on_message(client, userdata, message):
    global seconds
    global humidities
    global max_humidity
    global is_showering
    data = json.loads(message.payload)
    humidity = data["humidity"]
    timestamp = data["time"]
    humidities.append(humidity)
    elapsed_time=timestamp-start_time
    seconds.append(elapsed_time)
    print("Humidity",humidity)
    print("Time elapsed", elapsed_time)
    if humidity > max_humidity:
    	max_humidity=humidity
    if max_humidity-humidities[0] >=10:
    	is_showering = True
    	t1 = elapsed_time
    if is_showering and max_humidity - humidity >= 10:
        is_showering = False
        t2=elapsed_time
        client.disconnect()
        plt.plot(seconds, humidities)
        plt.xlabel("Time")
        plt.ylabel("Humidity (%)")
        plt.ylim(0, 100)  # Set y-axis limit to 0-100
        plt.title("Humidity Over Time during a shower")
        plt.show()

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_addy, broker_port, 60)
client.loop_forever()
