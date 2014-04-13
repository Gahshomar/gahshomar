Persian Calendar
================

A Persian (Jalali/Farsi) calendar which provides a basic app-indicator in Unity 
Desktop Environment.


Requirements
================

python-appindicator

Khayyam python package (http://pythonhosted.org/Khayyam/)


Installation
================

First make sure *Khayyam* and *python-appindicator* is installed:

    sudo apt-get install python-pip python-appindicator
    sudo pip install Khayyam

Download Persian calendar:

    cd ~
    wget -O persian-calendar.tar.gz https://github.com/183amir/persian-calendar/tarball/master
    mkdir persian-calendar
    tar -xf persian-calendar.tar.gz -C persian-calendar --strip-components 1
    cd persian-calendar
    chmod +x persian-calendar.py

Now press Alt+F2 and run the program from there by pasting the below command:

    ~/persian-calendar/persian-calendar.py

To make the program run when you login:

In Ubuntu, run *Startup Applications* and press add

Name:

    persian-calendar

Command:

    /usr/bin/env python ~/persian-calendar/persian-calendar.py

Comment:

    Persian Calendar Indicator


Support or Contact
================

Having troubles? Fill an issue at *https://github.com/183amir/persian-calendar*
or Contact me at *183.amir@gmail.com*.