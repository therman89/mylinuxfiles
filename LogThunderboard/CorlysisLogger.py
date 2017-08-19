import time
import requests
import argparse
import ConfigParser
import pygatt
import struct

config = ConfigParser.ConfigParser()
config.read("sensors.cfg")
node_addresses = config.get('Nodes', 'node_addresses').split(',')
uuid = dict()
uuid['temperature'] = config.get('uuid', 't_uuid')
uuid['humidity'] = config.get('uuid', 'rh_uuid')
uuid['supply_voltage'] = config.get('uuid', 'vsup_uuid')
uuid['als_reading'] = config.get('uuid', 'als_uuid')
uuid['uv_index'] = config.get('uuid', 'uv_uuid')
URL = 'https://corlysis.com:8086/write'
adapter = pygatt.GATTToolBackend()


def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument("db", help="TBS_1")
    # parser.add_argument("token", help="2ba7bbbaebe741e70c3fbdb817080d24")
    # args = parser.parse_args()
    db = "TBS_1"
    token = "2ba7bbbaebe741e70c3fbdb817080d24"
    corlysis_params = {"db": db, "u": "token", "p": token, "precision": "s"}

    unix_time_ms = int((time.time()-time.altzone))
    # read sensor data and convert it to line protocol
    # line = "sensors_data temperature={},pressure={},humidity={} {}\n".format(temperature,
    #                                                                          pressure,
    #                                                                          humidity,
    #                                                                          unix_time_ms)

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
            payload = "sensors_data temperature={},humidity={},supply_voltage={},ambient_light={}," \
                      "uv_index={} {}".format(temperature, humidity, supply_voltage,
                                              ALS, uv, unix_time_ms)
	    print payload
            r = requests.post(URL, params=corlysis_params, data=payload)
            print "Request sent:", r
            if r.status_code != 204:
                raise Exception("data not written")
	    break
        except pygatt.exceptions.NotificationTimeout:
            print "Timeout... retry"
	except pygatt.exceptions.NotConnectedError:
	   print "Not connected. Retrying..."
        finally:
            adapter.stop()


if __name__ == "__main__":
    main()
