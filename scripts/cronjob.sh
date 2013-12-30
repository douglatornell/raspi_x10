HEYU=/usr/local/bin/heyu
HEYU_CONFIG=/home/pi/.heyu/x10config
UPLOAD_SCHEDULE=/home/pi/raspi_x10/scripts/upload_schedule.sh
DOT_HEYU=/home/pi/.heyu

@reboot $HEYU -c $HEYU_CONFIG start

@midnight $UPLOAD_SCHEDULE > $DOT_HEYU/cronjob.out 2> $DOT_HEYU/cronjob.err
