Persian Calendar
================

A Persian (Jalali/Farsi) calendar which provides a basic appindicator.
(It has been tested on Unity, Gnome-shell, and XFCE but it should run on all
Desktop Environment as long as you have the libappindicator.)


Screenshot
================
![screenshot](data/Screenshot.png)


Requirements
================

python-appindicator

Khayyam python package (http://pythonhosted.org/Khayyam/)


Installation
================

Note: Arch Linux users can install it from AUR (https://aur.archlinux.org/packages/persian-calendar/)

First make sure *Khayyam* and *python-appindicator* is installed:

    sudo apt-get install python-pip python-appindicator
    sudo pip install Khayyam

Download Persian calendar (make sure all steps run successfully):

    sudo mkdir -p /opt/persian-calendar
    sudo chmod 775 /opt/persian-calendar
    wget -O persian-calendar.tar.gz https://github.com/183amir/persian-calendar/tarball/master
    sudo tar -xf persian-calendar.tar.gz -C /opt/persian-calendar --strip-components 1
    sudo install -Dm644 /opt/persian-calendar/persian-calendar.desktop /usr/share/applications/persian-calendar.desktop
    sudo install -Dm644 /opt/persian-calendar/data/icons/ubuntu-mono-dark/persian-calendar-`date +%d`.png /usr/share/pixmaps/persian-calendar.png
    sudo install -D -m644 /opt/persian-calendar/LICENSE /usr/share/licenses/persian-calendar/LICENSE
    sudo chmod +x /opt/persian-calendar/persian-calendar.py

Note: you can run the application from your applications menu (where you find your installed apps). 
Or, you could press Alt+F2 and run this command:

    /opt/persian-calendar/persian-calendar.py


Run at startup
================

To make the program run when you login:

    cp /usr/share/applications/persian-calendar.desktop ~/.config/autostart/

Support or Contact
================

Having troubles? Fill an issue at *https://github.com/183amir/persian-calendar*
or Contact me at *183.amir@gmail.com*.
