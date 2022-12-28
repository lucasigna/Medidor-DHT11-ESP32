import urequests
import json
import dht
from machine import Pin
from time import sleep

wifi_essid = 'XXXXXXXX'
wifi_pass = 'XXXXXXX'

sensor = dht.DHT11(Pin(14))

#Conectar a WiFi
def conectarWifi():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect( wifi_essid, wifi_pass)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

def send_data_to_firebase(data):
  url = "https://XXXXXXXXXXXXXX.firebaseio.com/data.json"
  headers = {"Content-Type": "application/json"}
  data = json.dumps(data)
  res = urequests.put(url, data=data, headers=headers)
  print(res.text)
  res.close()

conectarWifi()

while True:
    sensor.measure() # Mido los valores
    temp = sensor.temperature()
    humidity = sensor.humidity()
    data = {"temperature": temp, "humidity": humidity}
    send_data_to_firebase(data) # Envío los datos a la base de datos
    sleep(5)