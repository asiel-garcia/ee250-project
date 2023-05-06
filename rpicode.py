import grovepi
import math
import time
import paho.mqtt.client as mqtt
import json
import socket

sensor = 3
blue = 0
time_list = []
temp_list = []
hum_list = []
is_running = False

broker_addy = "172.20.10.10"
broker_port = 1883
username = "asielgar"
pwd = "12345"
topic = "Shower time"

client = mqtt.Client()
client.username_pw_set(username, pwd)
client.connect(broker_addy, broker_port, 60)

client.loop_start()

while True:
    try:
        [temp, hum] = grovepi.dht(sensor, blue)
        print("temp=%.02f C humidity=%.02f%%" % (temp, hum))
        data = {
            "time": time.time(),
            "temperature": temp,
            "humidity": hum
        }
        client.publish(topic, json.dumps(data))
        time.sleep(1)
    except KeyboardInterrupt:
        client.loop_stop()
        break
    except Exception as e:
        print("Error: ", str(e))
        client.disconnect()
        client.loop_stop()
        break
