# Raspberry Pi E-paper Monitor

A simple monitor displaying program for Raspberry Pi as a Downloader.

![](https://raw.githubusercontent.com/victrid-dev/victrid-dev.github.io/master/src/rpi-epaper-monitor.jpg)

## Recent Update:

Added a special power off display page.

You may establish a service to run poweroff service automatically. See [this](https://www.golinuxcloud.com/run-script-with-systemd-before-shutdown-linux/).

## Usage:

- Just run the ./main.py with python3
- ~~Or import this module, and run with main.write('WRITESOMETHING').~~
  - ~~It's sad that you can only write to the screen once, or it will say "Bad file descriptor" and I've got no Idea why.~~
  - Please refer to `power_critical.py`. I've got no idea how python's packages are packaged.

## Using:

- Raspberry Pi Zero W
- Waveshare 2.13inch e-Paper HAT (C)

## Dependencies:

- Driver
  - `sudo raspi-config`: Interfacing Options -> SPI -> Yes
  - BCM2835:
  ```
  wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.60.tar.gz
  tar zxvf bcm2835-1.60.tar.gz
  cd bcm2835-1.60/
  sudo ./configure
  sudo make
  sudo make check
  sudo make install
  ```
  - APT: `sudo apt install wiringpi python3-pip python3-pil python3-numpy`
  - GPIO Update:
  ```
  wget https://project-downloads.drogon.net/wiringpi-latest.deb
  sudo dpkg -i wiringpi-latest.deb
  ```
  - PIP: `sudo pip3 install RPi.GPIO spidev`
