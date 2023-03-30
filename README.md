# pylx16a-RPI
RPI environment for pylx16a

## Raspberry-Pi system info

Follow  https://ubuntu.com/download/raspberry-pi to install Ubuntu 22.10 LTS desktop version on the Raspberry Pi. You can check with the following command:
~~~
xinhao@ubuntu:~/pylx16a-RPI/scripts$ lsb_release -a
No LSB modules are available.
Distributor ID:	Ubuntu
Description:	Ubuntu 22.10
Release:	22.10
Codename:	kinetic
~~~

## PyLX16A Installation

### Prerequisites
~~~
sudo apt update;
sudo apt install -y gcc g++ make python3-dev python3-pip python3-pyqt6;
pip3 install pylx16a;
~~~

### Test pylx16a
~~~
xinhao@ubuntu:~/pylx16a-RPI/scripts$ python3
Python 3.10.7 (main, Mar 10 2023, 10:47:39) [GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pylx16a
>>>
~~~

### USB serial port issue
BRLTTY may cause the USB device (the linker) keeps disconnecting from the RPI, disable the rules and brltty service (copy and paste the command to the terminal):

~~~
for f in /usr/lib/udev/rules.d/*brltty*.rules; do
    sudo ln -s /dev/null "/etc/udev/rules.d/$(basename "$f")"
done
~~~
~~~
sudo udevadm control --reload-rules;
sudo systemctl mask brltty.path;
~~~


There should be no error message for the above command.

## Wireless Setup

First, please use monitor/keyboard/mouse to set up your RPi and connect to some Wifi (or your personal hotspot).

### SSH 
Then, enable SSH on RPI.

~~~
sudo apt install openssh-server;
sudo systemctl enable ssh && sudo system start ssh;
ip a;  # please select the ip address of the correct interface (usually wlan0 if it is connected to WIFI)
~~~ 

Connect to the RPI from your laptop (in the same local area network, e.g., DukeBlue)
~~~
ssh [username]@[ip]
~~~ 

Or use `putty` if you are using Windows.

### Send IP Address through Email when Boot Up.

You can also enable the Raspberry Pi to get its ip address and send you a email about the addresses and the wifi it connects to.

First please set up email service on your RPI
~~~
# install light SMTP (simple mail transfer protocol) client
sudo apt-get install msmtp; 

# **Edit!!**
# and copy the rc file to your home directory 
cp ./config/.msmtprc ~/.msmtprc; 

# If you wish to enable the email as a system service, please also copy the rc file to /etc/
sudo cp ./config/.msmtprc /etc/msmtprc;
~~~ 

Edit and copy the TellMeIP script to the correct place (e.g., under your home directory). The path should be aligned with the later .service file.

~~~
cp ./scripts/tellMeIp.sh ~/;
~~~

Enable a system service that run this script after it is connected to the network (network-online.target).

**Note: please make sure edit all the files based on your system (e.g., path name) before you run the `cp` command.**

~~~
sudo cp ./config/TellMeIP.service /etc/systemd/system/TellMeIP.service;
sudo systemctl daemon-reload;
sudo systemctl enable TellMeIP.service;
~~~

reboot with `sudo reboot` and check if you receive the email correctly. If you don't receive an email, please run the following command to see what is the error message.
~~~ 
sudo systemctl status TellMeIP.service
~~~

Now you should be able to receive a email whenever your Raspberry Pi is up, and you can connect to your Rpi in the same WLAN (included in the email) with the IP address (also in the email).

## Contact

Xinhao Kong (xinhao.kong@duke.edu)

## Reference

1. https://github.com/ethanlipson/PyLX-16A/

2. https://packages.ubuntu.com/search?keywords=python3-pyqt6

3. https://unix.stackexchange.com/questions/670636/unable-to-use-usb-dongle-based-on-usb-serial-converter-chip
