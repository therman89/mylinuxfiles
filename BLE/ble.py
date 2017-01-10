import pygatt
import binascii

adapter = pygatt.GATTToolBackend('hci1')
uuid_sw = "4331205c-a281-472f-abb4-35a6e79a094e"
try:
    adapter.start()
    device = adapter.connect('00:0B:57:06:17:4F')# EFR32MG
    #device = adapter.connect('00:0B:57:07:35:cF')  # TBS
    # for uuid in  device.discover_characteristics():
    #     print uuid
    value = device.char_read(uuid_sw)[0]
    device.char_write(uuid_sw,[1],True)

except Exception as e:
    print str(e)
    pass



finally:
    adapter.stop()