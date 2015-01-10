import datetime
from gettext import gettext as _
import logging
logger = logging.getLogger(__name__)

from gi.repository import GObject, Peas, Gtk, Gio, GLib

from gahshomar import log
from gahshomar import khayyam


class AppindicatorPlugin(GObject.Object, Peas.Activatable):
    __gtype_name__ = 'AppindicatorPlugin'

    object = GObject.property(type=GObject.Object)

    @log
    def do_activate(self):
        try:
            from gi.repository import AppIndicator3 as appindicator
        except ImportError:
            logger.exception(ImportError)
            return

        if hasattr(self, 'ind'):
            self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
            self.timer_id = GLib.timeout_add_seconds(5, self.update)
            return

        self.date = datetime.date.today()
        self.app = self.object

        self.settings = Gio.Settings.new('org.gahshomar.Gahshomar')
        self.date_format = str(self.settings.get_value('persian-date-format'))
        self.date_format = self.date_format.replace("'", "")

        self.ind = appindicator.Indicator.new(
            "GahShomar-indicator",
            'gahshomar',
            appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)

        self.menu_setup()
        self.update()

        self.timer_id = GLib.timeout_add_seconds(5, self.update)

    @log
    def menu_setup(self):
        self.menu = Gtk.Menu()
        self.menu.set_halign(Gtk.Align.CENTER)

        self.today_item = Gtk.MenuItem(_('Today'))
        self.today_item.connect("activate", self.activate)
        self.today_item.show()

        self.quit_item = Gtk.MenuItem(_('Quit'))
        self.quit_item.connect("activate", self.quit)
        self.quit_item.show()

        self.menu.append(self.today_item)
        self.menu.append(self.quit_item)
        self.ind.set_menu(self.menu)

    @log
    def get_date_formatted(self, frmt=None):
        if frmt is None:
            frmt = self.date_format
        text = khayyam.JalaliDate.from_date(self.date).strftime(frmt)
        if text[0] == '0' or text[0] == '۰':
            text = text[1:]
        return text

    @log
    def quit(self, widget):
        self.app.quit()

    @log
    def update(self):
        self.date = datetime.date.today()
        self.today_item.set_label(_(self.get_date_formatted()))
        self.ind.set_label(_(self.get_date_formatted('%d')), _('Gahshomar'))

        # make sure to return True so that it keeps updating
        return True

    @log
    def activate(self, *args):
        self.app.do_activate(self.app)

    @log
    def do_deactivate(self):
        try:
            from gi.repository import AppIndicator3 as appindicator
        except ImportError:
            logger.exception(ImportError)
            return
        if hasattr(self, 'ind'):
            self.ind.set_status(appindicator.IndicatorStatus.PASSIVE)
        GLib.source_remove(self.timer_id)

    @log
    def do_update_state(self):
        self.update()
