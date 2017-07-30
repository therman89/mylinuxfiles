import ConfigParser
import pygatt
import struct
from influxdb import InfluxDBClient
import datetime
import pytz

config = ConfigParser.ConfigParser()
config_path = "/home/pi/mylinuxfiles/LogThunderboard/sensors.cfg" 
config.read(config_path)
node_addresses = config.get('Nodes', 'node_addresses').split(',')
uuid = dict()
uuid['temperature'] = config.get('uuid', 't_uuid')
uuid['humidity'] = config.get('uuid', 'rh_uuid')
uuid['supply_voltage'] = config.get('uuid', 'vsup_uuid')
uuid['als_reading'] = config.get('uuid', 'als_uuid')
uuid['uv_index'] = config.get('uuid', 'uv_uuid')
adapter = pygatt.GATTToolBackend()


def main():

#    unix_time_ms = int((time.time()-time.altzone))

    d = datetime.datetime.utcnow()
    unix_time_ms = d.replace(tzinfo=pytz.UTC)
    unix_time_ms.isoformat()
    while True:
        try:
            adapter.start()
#            print "Adapter started. Connecting to", node_addresses[1]
            device = adapter.connect(node_addresses[0])  # TBS
#            print "connected to BLE device"
            humidity = struct.unpack("<H", device.char_read(uuid['humidity']))[0] / 100.0
            temperature = struct.unpack("<H", device.char_read(uuid['temperature']))[0] / 100.0
            supply_voltage = struct.unpack("<H", device.char_read(uuid['supply_voltage']))[0] / 1000.0
            ALS = struct.unpack("<H", device.char_read(uuid['als_reading']))[0]
            uv = struct.unpack("<B", device.char_read(uuid['uv_index']))[0]
            device.disconnect()
	    payload = {'temperature':temperature,
		        'humidity':humidity,
        		'supply-voltage':supply_voltage,
        		'ambient-light':ALS,
        		'uv-index':uv}	
	        
	    json_body = [
                {
                "measurement": "TBS_1",
		'tags':{
			'device':node_addresses[0],
			'location':'Bedroom'
		},
		'fields':{
			'temperature':temperature,
                        'humidity':humidity,
                        'supply-voltage':supply_voltage,
                        'ambient-light':ALS,
                        'uv-index':uv
			}
                }
            ]
	    print json_body
        
            client = InfluxDBClient('localhost', 8086, 'admin', 'tiDO1989', 'test')
            client.write_points(json_body)

	    break 

        except pygatt.exceptions.NotificationTimeout:
	    pass
#            print "Timeout... retry"
	except pygatt.exceptions.NotConnectedError:
	    pass#print "Not connected. Retrying..."
        finally:
            adapter.stop()


if __name__ == "__main__":
    main()
