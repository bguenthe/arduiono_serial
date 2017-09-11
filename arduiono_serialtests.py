import json

import serial
import paho.mqtt.client as mqtt

arduino = serial.Serial('COM5', 9600)
while True:
    data = arduino.readline()
    print(data)