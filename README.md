persian-calendar
================

A Persian (Jalali/Farsi) calendar which provides a basic app indicator in Unity Desktop Environment.


Requirements
================
Python 2
Khayyam python package (http://pythonhosted.org/Khayyam/)


Installation
================
First make sure Khayyam is installed:
sudo apt-get install python-pip
sudo pip install Khayyam

Clone the repository:
	cd ~
	git clone https://github.com/183amir/persian-calendar.git
	cd persian-calendar
	chmod +x persian-calendar.py
Now press Alt+F2 and run the program from there:
	~/persian-calendar/persian-calendar.py

To make the program run when you login:
In Ubuntu, run 'Startup Applications' and press add
Name:
	persian-calendar
Command:
	/usr/bin/env python ~/persian-calendar/persian-calendar.py
Comment:
	Persian Calendar Indicator