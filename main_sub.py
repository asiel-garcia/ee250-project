import paho.mqtt.client as mqtt
import json
import matplotlib.pyplot as plt
import time
import numpy as np

broker_addy = "172.20.10.10"
broker_port = 1883
username = "asielgar"
pwd = "12345"
topic = "Shower time"
humidities = []
seconds = []
max_humidity=0
is_showering=False
flag1=False
flag2=False

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
    global flag1
    global flag2
    global t1
    data = json.loads(message.payload)
    humidity = data["humidity"]
    timestamp = data["time"]
    humidities.append(humidity)
    elapsed_time=timestamp-start_time
    seconds.append(elapsed_time)
    #print("Humidity",humidity)
    #print("Time elapsed", elapsed_time)
    if humidity > max_humidity:
        max_humidity=humidity
    if max_humidity-humidities[0] >=15 and not flag1:
        is_showering = True
        t1 = elapsed_time
        flag1=True
    if is_showering and max_humidity - humidity >= 10 and not flag2:
        is_showering = False
        t2=elapsed_time
        flag2=True
        client.disconnect()
        print("This is the time spent showering in seconds")
        print(t2-t1)
        sec_arr = np.array(seconds)
        hum_arr = np.array(humidities)
        plt.plot(sec_arr, hum_arr)
        plt.fill_between(sec_arr, hum_arr, where=((sec_arr>=t1)&(sec_arr<=t2)), color='gray', alpha=0.5)
        plt.axvline(x=t1, color='b', linestyle='--',label='Shower start')
        plt.axvline(x=t2, color='g', linestyle='--',label='Shower end')
        plt.xlabel("Time")
        plt.ylabel("Humidity (%)")
        plt.ylim(0, 100)
        plt.title("Humidity Over Time during a shower")
        plt.legend()
        plt.show()

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_addy, broker_port, 60)
client.loop_forever()
