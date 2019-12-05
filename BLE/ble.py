import pygatt
import binascii
import struct
import json

adapter = pygatt.GATTToolBackend('hci0')
uuid_temp = "2a6e"
uuid_rh = "2a6f"
uuid_supply = "bc2bd1b4-e18f-4fcc-8c21-f44e9b07af21"
adapter.start()
#device = adapter.connect('00:0b:57:51:af:de') # EFR32MG
device = adapter.connect('00:0B:57:10:1A:61') # EFR32MG
print "Connected"
#device = adapter.connect('00:0B:57:07:35:cF')  # TBS
#for uuid in  device.discover_characteristics():
#    print uuid
temp =  struct.unpack("<H",device.char_read(uuid_temp, timeout=5))[0]/100.0
rh = struct.unpack("<H",device.char_read(uuid_rh, timeout=5))[0]/100.0
supply = struct.unpack("<H",device.char_read(uuid_supply, timeout=5))[0]/1000.0
json_dump = 	{
		"Temperature":temp,
		"Humidity":rh,
		"SupplyVoltage":supply
		}
with open("sensor.json","a") as f:
	json.dump(json_dump, f)
	f.write("\n")
print temp, rh, supply

