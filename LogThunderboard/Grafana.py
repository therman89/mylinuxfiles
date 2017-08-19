# -*- coding: utf-8 -*-
# #!/usr/bin/env python
import ConfigParser
import pygatt
import struct
from influxdb import InfluxDBClient
import datetime
import pytz
import pyowm
import urllib2
from BeautifulSoup import BeautifulSoup

config = ConfigParser.ConfigParser()
config_path = "/home/pi/mylinuxfiles/LogThunderboard/sensors.cfg" 
config.read(config_path)
node_addresses = config.get('Nodes', 'node_addresses').split(',')
node_locations = config.get('Nodes', 'node_locations').split(',')
nodes = {'address':node_addresses, 'location':node_locations}
uuid = dict()
uuid['temperature'] = config.get('uuid', 't_uuid')
uuid['humidity'] = config.get('uuid', 'rh_uuid')
uuid['supply_voltage'] = config.get('uuid', 'vsup_uuid')
uuid['als_reading'] = config.get('uuid', 'als_uuid')
uuid['uv_index'] = config.get('uuid', 'uv_uuid')
adapter = pygatt.GATTToolBackend()
temperature_external = None
try:
	owm = pyowm.OWM('cdb3776f739eb81734fcd21f893ccc21')
	observation = owm.weather_at_place('Budapest')
	w = observation.get_weather()
	temperature_external = w.get_temperature('celsius')['temp']
except:
	pass
def main():

#    unix_time_ms = int((time.time()-time.altzone))
	adapter.start()
#   print "Adapter started. Connecting to", node_addresses[1]
	for i in range(len(nodes)):
		retry = 3
		while retry:
			retry -= 1
			try:
				#Iterate all Thunderboard Senses
#				print nodes['address'][i]
				device = adapter.connect(nodes['address'][i])  # TBS
	#            print "connected to BLE device"
				#Get data from one Thunderboard Sense
				humidity = struct.unpack("<H", device.char_read(uuid['humidity']))[0] / 100.0
				temperature = struct.unpack("<H", device.char_read(uuid['temperature']))[0] / 100.0
				supply_voltage = struct.unpack("<H", device.char_read(uuid['supply_voltage']))[0] / 1000.0
				ALS = struct.unpack("<H", device.char_read(uuid['als_reading']))[0]
				uv = struct.unpack("<B", device.char_read(uuid['uv_index']))[0]
				device.disconnect()
				d = datetime.datetime.utcnow()
				unix_time_ms = d.replace(tzinfo=pytz.UTC)
				unix_time_ms.isoformat()
				
				json_body = [
						{
						"measurement": "TBS_1",
				'tags':{
					'device':nodes['address'][i],
					'location':nodes['location'][i]
				},
				'fields':{
					'temperature':temperature,
					'humidity':humidity,
					'supply-voltage':supply_voltage,
					'ambient-light':ALS,
					'uv-index':uv,
					'temperature-outside':temperature_external
					}
						}
					]
#				print json_body
			
				client = InfluxDBClient('localhost', 8086, 'admin', 'tiDO1989', 'test')
				client.write_points(json_body)
				break
			except pygatt.exceptions.NotificationTimeout:
				pass
			#   print "Timeout... retry"
			except pygatt.exceptions.NotConnectedError:
				pass
				#print "Not connected. Retrying..."			
	
	adapter.stop()

        
def get_weather():
	pass


if __name__ == "__main__":
    main()
