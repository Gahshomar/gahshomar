#!/usr/bin/env python3

# Copyright (C) 2004-2006 Red Hat Inc. <http://www.redhat.com/>
# Copyright (C) 2005-2007 Collabora Ltd. <http://www.collabora.co.uk/>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use, copy,
# modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from gettext import gettext as _
import logging
logger = logging.getLogger(__name__)

from gi.repository import GObject, Gio
import dbus
import dbus.service

from gahshomar.khayyam import JalaliDate


class DemoException(dbus.DBusException):
    _dbus_error_name = 'com.example.DemoException'


class IndicatorBus(dbus.service.Object):

    def __init__(self, *args, app=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.settings = Gio.Settings.new('org.gahshomar.Gahshomar')
        try:
            self.date_format = str(
                self.settings.get_value('persian-date-format'))
            self.date_format = self.date_format.replace("'", "")
        except Exception:
            logger.exception(Exception)
            self.date_format = '%A، %d %B %Y'

    @dbus.service.method("org.gahshomar.IndicatorInterface",
                         in_signature='', out_signature='s')
    def GetDayNumber(self):
        day = JalaliDate.today().strftime('%d')
        if day[0] == '۰':
            day = day[1:]
        return day

    @dbus.service.method("org.gahshomar.IndicatorInterface",
                         in_signature='', out_signature='s')
    def GetDateFormatted(self):
        return JalaliDate.today().strftime(self.date_format)

    @dbus.service.method("org.gahshomar.IndicatorInterface",
                         in_signature='', out_signature='')
    def ActivateApp(self):
        self.app.do_activate()

    @dbus.service.method("org.gahshomar.IndicatorInterface",
                         in_signature='', out_signature='')
    def ExitApp(self):
        self.app.quit()

    @dbus.service.method("org.gahshomar.IndicatorInterface",
                         in_signature='', out_signature='s')
    def GetQuitString(self):
        return _('Quit')


if __name__ == '__main__':
    import dbus.mainloop.glib
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    session_bus = dbus.SessionBus()
    # name = dbus.service.BusName("org.gahshomar.Gahshomar", session_bus)
    name = dbus.service.BusName("org.gahshomar.GahshomarService", session_bus)
    dbus_object = IndicatorBus(session_bus, '/IndicatorBus')

    mainloop = GObject.MainLoop()
    print("Running example service.")
    mainloop.run()
