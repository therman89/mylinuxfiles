import pygatt
import binascii
import struct
import json
import sys
import os

adapter = pygatt.GATTToolBackend('hci0')
uuid_temp = "2a6e"
uuid_rh = "2a6f"
uuid_supply = "bc2bd1b4-e18f-4fcc-8c21-f44e9b07af21"
adapter.start()
device_address = sys.argv[2]
device_id =  sys.argv[1]
print "address", device_address, "id", device_id
#device = adapter.connect('00:0b:57:51:af:de') # EFR32MG
#device = adapter.connect('00:0B:57:10:1A:61') # EFR32MG
try:
	device = adapter.connect(device_address) # Not checked against errors
	print "Connected"
	temp =  struct.unpack("<H",device.char_read(uuid_temp, timeout=5))[0]/100.0
	rh = struct.unpack("<H",device.char_read(uuid_rh, timeout=5))[0]/100.0
	supply = struct.unpack("<H",device.char_read(uuid_supply, timeout=5))[0]/1000.0
	print temp, rh, supply
finally:
	adapter.stop()
	print "Disconnected"
f_thunderboard_json = os.path.dirname(os.path.realpath(__file__))+"/Thunderboard.json"
line=""
with open(f_thunderboard_json, 'r') as f:
	line = f.readline()
data = json.loads(line)
print data
#	json_dump = 	{
#		"Thunderboard_1": {
#			"Temperature":temp,
#			"Humidity":rh,
#			"SupplyVoltage":supply
#			},
#		"Thunderboard_2":{ 
#			"Temperature":temp,
#			"Humidity":rh,
#			"SupplyVoltage":supply
#			}
#		}
data[device_id]["Temperature"]=temp
data[device_id]["Humidity"]=rh
data[device_id]["SupplyVoltage"]=supply
with open(f_thunderboard_json, 'w') as f:
	json.dump(data, f)

