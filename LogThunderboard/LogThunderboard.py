import serial
from time import sleep 
import urllib
import urllib2
#import requests
import re
from datetime import datetime
import pygatt
import struct
class Measurement():
	ReadKey = 0
Node = [Measurement()]
#Node[0].ReadKey = 'DW24J25W85FHJ6XD'
Node[0].ReadKey = 'M6UVE1VBFQGNHNDI'

adapter = pygatt.GATTToolBackend()

t_uuid = '2a6e'#-0000-1000-8000-00805f9b34fb'
rh_uuid = '2a6f'#-0000-1000-8000-00805f9b34fb'
v_uuid = '5c44409f-b4f4-41d4-8625-0630bb5f544b'
als_uuid = '5d34b788-3315-47e8-89c8-08d3a95d72b6'
uv_uuid = '2a76'#-0000-1000-8000-00805f9b34fb'
#      	for char in device.discover_characteristics():
#		print char

#while True:

while True:
	try:
		adapter.start()
#		print "Adapter started"
	      # device = adapter.connect('00:0B:57:07:35:CF')#TBS
    		device = adapter.connect('00:0B:57:51:AF:DE')  # TBS
#		print "connected to BLE device"
		Node[0].humidity = humidity = struct.unpack("<H", device.char_read(rh_uuid))[0]/100.0
		Node[0].temp = temperature = struct.unpack("<H", device.char_read(t_uuid))[0]/100.0
		Node[0].Vbat = supply_voltage = struct.unpack("<H", device.char_read(v_uuid))[0]
		Node[0].ALS = ALS = struct.unpack("<H", device.char_read(als_uuid))[0]
		Node[0].UV = uv = struct.unpack("<B", device.char_read(uv_uuid))[0]
		device.disconnect()

#      		print "Temperature: {}, Humidity: {}, Supply Voltage: {}mV,"\
#			"Ambient light: {} lux, UV index: {}"\
#	       		 .format(temperature, humidity, supply_voltage, ALS, uv)

		params = urllib.urlencode({'key': Node[0].ReadKey, 
				'field1': Node[0].temp,
				'field2': Node[0].humidity,
				'field3': Node[0].ALS,
				'field4': Node[0].UV,
				'field5': Node[0].Vbat})
		ret = urllib.urlopen("https://api.thingspeak.com/update", 
			data=params)
		break
		#print ret
		#raw_input("Press enter for next...")
	except pygatt.exceptions.NotificationTimeout:
      		print "Timeout... retry"
	finally:
      		adapter.stop()



