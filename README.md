"# HRWOXNS" 

(Hori Racing Wheel Overdrive for Xbox on Nintendo Switch)

A big thanks to mart1nro for his awesome bluetooth joycon emulator
https://github.com/mart1nro/joycontrol/issues

This project was built on mart1nro's joycontrol, it reads the USB serial port for any HORI Overdrive for XBOX series | S and sends the commands as a wireless nintendo switch controller.

It auto connects to my switch 58:B0:3E:07:25:14 for now because I'm lazy, if you want to test this script, replace this with your switch's bluetooth address in code.

The script assumes your nintendo switch is already on, and your HORI steering wheel already connected to your raspberry PI.

This project depends on pyusb
https://github.com/pyusb/pyusb

Note: This script is absolutely no necesary for playing mario kart with a steering wheel, there are nintendo ready steering wheels out there for about 120 bucks.

