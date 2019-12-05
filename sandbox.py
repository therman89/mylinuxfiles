import paho.mqtt.publish as publish
from time import sleep
for i in range(1,10):
	print i
	msgs = [("house/LV_switch/cmnd/dimmer", str(i), 0, False)]
	publish.multiple(msgs, hostname="192.168.1.10", port=1883)
	sleep(0.2)




