from gettext import gettext as _

from gi.repository import GObject, Peas, Gtk

from gahshomar import log


class NoHeaderBarPlugin(GObject.Object, Peas.Activatable):
    __gtype_name__ = 'NoHeaderBarPlugin'

    object = GObject.property(type=GObject.Object)

    @log
    def do_activate(self):
        self.win = self.object._window
        self.prefs = self.object.setting_win
        self.hb = self.win.hb
        self.win.set_titlebar(None)
        toolbar = Gtk.Toolbar()
        self.toolbar = toolbar
        tb_today = Gtk.ToolButton(label=_('Today'))
        tb_today.set_action_name('win.today')
        toolbar.add(tb_today)
        toolbar.show_all()
        self.win.main_grid.insert_row(0)
        self.win.main_grid.attach(toolbar, 0, 0, 2, 1)
        if self.prefs is not None:
            self.prefs.present()

    @log
    def do_deactivate(self):
        self.win.main_grid.remove_row(0)
        self.toolbar.destroy()
        self.win.set_titlebar(self.hb)
        if self.prefs is not None:
            self.prefs.present()

    @log
    def do_update_state(self):
        pass
