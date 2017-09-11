import json
import threading

import serial
import paho.mqtt.client as mqtt
import time

connected = False
client = None
arduino = None


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    topics = [("/arduino/ask_for_button_status", 0), ("/arduino/cycle", 0), ("/arduino/LEDswitch", 0)]

    client.subscribe(topics)
    print("Subscribed to: " + str(topics))


# Einkommende Kommandos, die für den Arduino bestimmt sind
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    message = msg.payload.decode()
    if msg.topic == "/arduino/ask_for_button_status":
        arduino.write("button_status\n".encode())
    elif msg.topic == "/arduino/cycle":
        arduino.write("cycle\n".encode())
    elif msg.topic == "/arduino/LEDswitch":
        arduino.write((message + "\n").encode())

def on_disconnect(client, userdata, rc):
    raise Exception


def mqtt_init():
    global client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    #    client.connect("raspberrypi-lan.lyk3nnyrasmj0efc.myfritz.net", 1883, 60)
    client.connect("192.168.178.33", 1883, 60)  # raspberrypi-lan
    # client.connect("192.168.178.21", 1883, 60)  # raspberrypi-wlan

    client.loop_start()


def serial_init():
    global arduino
    # arduino = serial.Serial('COM5', 9600, timeout=.1)
    arduino = serial.Serial('COM5', 9600)


# Daten vom Arduino auswerten und messages senden
def handle_data(data):
    try:
        jsondata = json.loads(data)
        if "/arduino/counter" in jsondata:
            client.publish("/arduino/counter", jsondata["/arduiono/counter"].value)
        elif "/arduino/button_status" in jsondata:
            client.publish("/arduino/button_status", jsondata["/arduino/button_status"])
    except Exception as e:
        print(e.__str__())


def read_from_port(arduino):
    global connected
    while not connected:
        connected = True

        while True:
            data = arduino.readline().decode()
            if data:
                handle_data(data)


# Daten an den arduino senden - wird momentan nicht benötigt
# def write_to_port(arduino):
#     global connected
#
#     while True:
#         time.sleep(10)
#         print("write")
#         arduino.write("tasterstatus\n".encode())

