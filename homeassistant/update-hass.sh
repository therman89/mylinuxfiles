#!/bin/bash
service home-assistant@homeassistant stop
cd /srv/homeassistant
source bin/activate
python3 -m pip install --upgrade homeassistant
service home-assistant@homeassistant start

