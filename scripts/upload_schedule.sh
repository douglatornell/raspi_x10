#!/bin/bash
# Calculate a HEYU schedule based on the state of the away mode device
# and upload it to the controller

RASPI_X10=/home/pi/raspi_x10
DEVICES=$RASPI_X10/heyu/x10_devices.py
SPECIAL_DAYS=$RASPI_X10/heyu/special_days.py
PYTHON=/usr/bin/python3
HEYU=/usr/local/bin/heyu
HEYU_CONFIG=/home/pi/.heyu/x10config

AWAY_MODE=$[ $($HEYU -c $HEYU_CONFIG onstate H16) ]
if [ $AWAY_MODE -eq "0" ]; then
    RULES=$RASPI_X10/heyu/people_home_rules.py
else
    RULES=$RASPI_X10/heyu/away_mode_rules.py
fi

cd $RASPI_X10 \
&& \
$PYTHON -m raspi_x10.schedule $DEVICES $RULES $SPECIAL_DAYS \
&& \
$HEYU -c $HEYU_CONFIG upload
