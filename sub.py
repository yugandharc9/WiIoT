import ubinascii
import machine
import micropython
import network

from umqtt.robust import MQTTClient
from machine import Pin
# ESP8266 ESP-12 modules have blue, active-low LED on GPIO2, replace
# with something else if needed.
led = Pin(12, Pin.OUT)

print('yes')
# Default MQTT server to connect to
SERVER = "www.thingslab.io"
CLIENT_ID = 'pyclient'
TOPIC = b"ESP-156"
state = 0

def sub_cb(topic, msg):
    global state
    print((topic, msg))
    if msg == b"0":
        led.value(0)
        state = 1
    elif msg == b"1":
        led.value(1)
        state = 0
    elif msg == b"toggle":
        # LED is inversed, so setting it to current state
        # value will make it toggle
        led.value(state)
        state = 1 - state


def main(server=SERVER):

    s=network.WLAN(network.STA_IF)
    s.active(True)
    #print(s.scan())
    s.connect('SSID','PASSWORD')
    c = MQTTClient(CLIENT_ID, server,port=1883,user="hi1",password="hello1")
    # Subscribed messages will be delivered to this callback1
    c.set_callback(sub_cb)
    c.connect()
    
    c.publish(r"ESP-156", r"yippe")
    c.subscribe(TOPIC)
    print("Connected to %s, subscribed to %s topic" % (server, TOPIC))
  
    try:
        while 1:
            #micropython.mem_info()
            c.wait_msg()
            if not c.connect(clean_session=False):
             print("New session being set up")
             c.subscribe(b"room/fire")

    finally:
        c.disconnect()

if __name__=="__main__":
 main()
