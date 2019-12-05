# -*- Mode: Python; coding: utf-8; indent-tabs-mode: s; tab-width: 4 -*-

from .calendar import TODAY_PERSIAN
from gi.repository import Gio, GLib


class Server(object):
    # copied from https://github.com/GNOME/gnome-
    # music/blob/41a77b1e44fa95aacf08cd9692fcd9e5b7917422/gnomemusic/mpris.py
    def __init__(self, con, path, **kwargs):
        super().__init__(**kwargs)
        method_outargs = {}
        method_inargs = {}
        for interface in Gio.DBusNodeInfo.new_for_xml(self.__doc__).interfaces:

            for method in interface.methods:
                method_outargs[method.name] = '(' + ''.join(
                    [arg.signature for arg in method.out_args]) + ')'
                method_inargs[method.name] = tuple(
                    arg.signature for arg in method.in_args)

            con.register_object(
                object_path=path,
                interface_info=interface,
                method_call_closure=self.on_method_call)

        self.method_inargs = method_inargs
        self.method_outargs = method_outargs

    def on_method_call(self, connection, sender, object_path, interface_name,
                       method_name, parameters, invocation):

        args = list(parameters.unpack())
        for i, sig in enumerate(self.method_inargs[method_name]):
            if sig == 'h':
                msg = invocation.get_message()
                fd_list = msg.get_unix_fd_list()
                args[i] = fd_list.get(args[i])

        result = getattr(self, method_name)(*args)

        # out_args is atleast (signature1). We therefore always wrap the result
        # as a tuple. Refer to
        # https://bugzilla.gnome.org/show_bug.cgi?id=765603
        result = (result, )

        out_args = self.method_outargs[method_name]
        if out_args != '()':
            variant = GLib.Variant(out_args, result)
            invocation.return_value(variant)
        else:
            invocation.return_value(None)


class GahshomarApi(Server):
    """
    <node>
        <interface name='org.gahshomar.Api'>
            <method name='GetDay'>
                <arg type='s' name='day' direction='out'/>
            </method>
            <method name='GetDate'>
                <arg type='s' name='date' direction='out'/>
            </method>
        </interface>
    </node>
    """

    def __init__(self, connection, object_path, **kwargs):
        super().__init__(connection, object_path, **kwargs)

    def GetDay(self):
        return TODAY_PERSIAN.day_str

    def GetDate(self):
        return TODAY_PERSIAN.full_date

    def Introspect(self):
        return self.__doc__
