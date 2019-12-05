import paho.mqtt.publish as publish
import sys

state = sys.argv[1]
msgs = [("house/christmas_lights/kitchen/cmnd/power", state, 0, False),
    ("house/christmas_lights/staircase/cmnd/power", state, 0, False),
    ("house/christmas_lights/livingroom/cmnd/power", state, 0, False),
    ("house/christmas_lights/bedroom/cmnd/power", state, 0, False)]
publish.multiple(msgs, hostname="192.168.1.10", port=1883)


