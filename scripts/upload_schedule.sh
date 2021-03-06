#!/bin/bash
# Calculate a HEYU schedule based on the state of the away mode device
# and upload it to the controller

HEYU=/usr/local/bin/heyu
AWAY_MODE_DEVICE=H16

PYTHON=/usr/bin/python3

RASPI_X10=/home/pi/raspi_x10
DEVICES=$RASPI_X10/heyu/x10_devices.py
SPECIAL_DAYS=$RASPI_X10/heyu/special_days.py

AWAY_MODE=$[ $($HEYU onstate $AWAY_MODE_DEVICE) ]
if [ $AWAY_MODE -eq "0" ]; then
    RULES=$RASPI_X10/heyu/people_home_rules.py
else
    RULES=$RASPI_X10/heyu/away_mode_rules.py
fi

cd $RASPI_X10 \
&& \
$PYTHON -m raspi_x10.schedule $DEVICES $RULES $SPECIAL_DAYS \
&& \
$HEYU upload
