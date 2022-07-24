Shutdown companion using RCx_OPTION.

# How to setup
```
$ cd
$ git clone https://github.com/tajisoft/pidown
$ sudo cp pidown/pidown.service /etc/systemd/system/
$ sudo systemctl enable pidown.service
(Option) Edit --connect option in start_pidown.sh if you need.
$ sudo systemctl start pidown.service
```

# How to use
Assume use RC6_OPTION to shutdown RPi.
1. set RC6_OPTION=47
2. Switch CH6 to high and wait 5 sec.

# Feedback
Any issue report or PR are welcome.

# License
MIT
