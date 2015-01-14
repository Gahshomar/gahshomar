from gettext import gettext as _

from gi.repository import GObject, Peas, Gio, GLib

from gahshomar import log


class NoHeaderBarPlugin(GObject.Object, Peas.Activatable):
    __gtype_name__ = 'NoHeaderBarPlugin'

    object = GObject.property(type=GObject.Object)

    @log
    def do_activate(self):
        self.settings = Gio.Settings.new('org.gahshomar.Gahshomar')
        self.settings.set_value('header-bar', GLib.Variant.new_boolean(True))

    @log
    def do_deactivate(self):
        self.settings.set_value('header-bar', GLib.Variant.new_boolean(False))

    @log
    def do_update_state(self):
        pass
