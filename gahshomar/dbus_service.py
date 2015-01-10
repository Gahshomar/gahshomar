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

from gahshomar import log
from gahshomar.khayyam import JalaliDate


# class IndicatorBus(GObject.Object):

#     @log
#     def __init__(self, *args, app=None, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.app = app
#         self.settings = Gio.Settings.new('org.gahshomar.Gahshomar')
#         try:
#             self.date_format = str(
#                 self.settings.get_value('persian-date-format'))
#             self.date_format = self.date_format.replace("'", "")
#         except Exception:
#             logger.exception(Exception)
#             self.date_format = '%A، %d %B %Y'
#         self.introspection_xml = '''
#             <node name="/IndicatorBus">
#               <interface name="org.gahshomar.Gahshomar.Indicator">
#                 <method name="GetQuitString">
#                   <arg direction="out" type="s" />
#                 </method>
#                 <method name="GetDateFormatted">
#                   <arg direction="out" type="s" />
#                 </method>
#                 <method name="GetDayNumber">
#                   <arg direction="out" type="s" />
#                 </method>
#                 <method name="ActivateApp">
#                 </method>
#                 <method name="ExitApp">
#                 </method>
#               </interface>
#             </node>'''.strip()

#     @log
#     def GetDayNumber(self):
#         day = JalaliDate.today().strftime('%d')
#         if day[0] == '۰':
#             day = day[1:]
#         return day

#     @log
#     def GetDateFormatted(self):
#         return JalaliDate.today().strftime(self.date_format)

#     @log
#     def ActivateApp(self):
#         self.app.do_activate()

#     @log
#     def ExitApp(self):
#         self.app.quit()

#     @log
#     def GetQuitString(self):
#         return _('Quit')


# class IndicatorVTable(Gio.DBusInterfaceVTable):
#     """docstring for IndicatorVTable"""
#     @log
#     def __init__(self):
#         super(IndicatorVTable, self).__init__()

#     @log
#     @classmethod
#     def handle_method_call(connection, sender, object_path,
#                            interface_name, method_name, parameters, invocation,
#                            user_data):
#      # func_names = [a for a in IndicatorBus.__dict__.keys() if not a[0] == '_']
#         # if method_name in func_names:
#         ret_value = user_data[method_name](parameters)
#         invocation.return_value(ret_value)

#     @log
#     @classmethod
#     def handle_get_property(*args):
#         pass

#     @log
#     @classmethod
#     def handle_set_property(*args):
#         pass

class IndicatorBus(dbus.service.Object):

    def __init__(self, app=None):
        self.app = app
        self.settings = Gio.Settings.new('org.gahshomar.Gahshomar')
        try:
            self.date_format = str(
                self.settings.get_value('persian-date-format'))
            self.date_format = self.date_format.replace("'", "")
        except Exception:
            logger.exception(Exception)
            self.date_format = '%A، %d %B %Y'
        import dbus.mainloop.glib
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        session_bus = dbus.SessionBus()
        self.bus_name = dbus.service.BusName("org.gahshomar.GahshomarService",
                                             session_bus)
        super().__init__(session_bus, '/org/gahshomar/Gahshomar')

    @dbus.service.method("org.gahshomar.Gahshomar.Indicator",
                         in_signature='', out_signature='s')
    def GetDayNumber(self):
        day = JalaliDate.today().strftime('%d')
        if day[0] == '۰':
            day = day[1:]
        return day

    @dbus.service.method("org.gahshomar.Gahshomar.Indicator",
                         in_signature='', out_signature='s')
    def GetDateFormatted(self):
        return JalaliDate.today().strftime(self.date_format)

    @dbus.service.method("org.gahshomar.Gahshomar.Indicator",
                         in_signature='', out_signature='')
    def ActivateApp(self):
        self.app.do_activate()

    @dbus.service.method("org.gahshomar.Gahshomar.Indicator",
                         in_signature='', out_signature='')
    def ExitApp(self):
        self.app.quit()

    @dbus.service.method("org.gahshomar.Gahshomar.Indicator",
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
