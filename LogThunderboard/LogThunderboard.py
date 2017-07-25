import serial
from time import sleep 
import urllib
import urllib2
#import requests
import re
from datetime import datetime
import pygatt
import struct

Node[0].ReadKey = 'DW24J25W85FHJ6XD'
Node[1].ReadKey = 'M6UVE1VBFQGNHNDI'

adapter = pygatt.GATTToolBackend()

t_uuid = '00002a6e-0000-1000-8000-00805f9b34fb'
rh_uuid = '00002a6f-0000-1000-8000-00805f9b34fb'
while True:
   try:
      adapter.start()
      # device = adapter.connect('00:0B:57:07:35:CF')#TBS
      device = adapter.connect('00:0B:57:51:AF:DE')  # TBS
      humidity = device.char_read(rh_uuid)
      temperature = device.char_read(t_uuid)
      device.disconnect()

      print "Temperature: {}, Humidity: {}"\
         .format(struct.unpack("<H", temperature)[0]/100.0,
               struct.unpack("<H", humidity)[0]/100.0)
      raw_input()
   finally:
      adapter.stop()



#while(True):
#
#		if(NumberOfLines ==  MEAS_DATA_LINES):			
#			params = urllib.urlencode({'key': Node[nodeidx].ReadKey, 
#				'field1': Node[nodeidx].temp,
#				'field2': Node[nodeidx].humidity,
#				'field3': Node[nodeidx].amblight,
#				'field4': Node[nodeidx].RSSI,
#				'field5': Node[nodeidx].Vbat})
#			ret = urllib.urlopen("https://api.thingspeak.com/update", 
#				data=params)
#	#		print ret
#	except IndexError:
#		with open("log.txt",'a') as log:
#			log.write(str(datetime.now()) + " Index error. Last data was:\n")
#			log.write(line + "\n")
#	except Exception as e:
#		with open("log.txt",'a') as log:
#			log.write(str(datetime.now()) + " Unhandled exception.\n" + str(e) + "\nLast data was:\n")
#			log.write(line + "\n")
#		

