#!/bin/bash

cp gws.py /home/fishineer/gew/weewx/bin/user
cd /home/fishineer/gew/weewx/bin/user
rm GWSDriver_old.py
mv GWSDriver.py GWSDriver_old.py
mv gws.py GWSDriver.py


