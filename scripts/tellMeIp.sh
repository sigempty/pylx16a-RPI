#!/bin/bash

# Get IP address
IP_ADDRESS=`hostname -I | awk '{print $1}'`
DATE=`date`
WIFI_NAME=`iwgetid`

str="Raspberry Pi is on. Date: $DATE \n
     Connect to: $WIFI_NAME \n
     IP: $IP_ADDRESS"
echo -e $str
# Send email
echo -e $str | msmtp xinhao.kong@duke.edu # send email to my duke email account
echo -e $str | msmtp sigempty@gmail.com   # send email to my gmail account 

# Enable USB permssion
chmod a+rw /dev/ttyUSB0
