from gettext import gettext as _
from gi.repository import Gtk, Gio, AppIndicator3
import logging
logger = logging.getLogger(__name__)


class AppIndicator(object):
    """Gahshomar's appindicator"""

    def __init__(self, application, calendar, **kwargs):
        super(AppIndicator, self).__init__(**kwargs)
        self.application = application
        self.calendar = calendar

        # setup the AppIndicator
        self.ind = AppIndicator3.Indicator.new(
            "Gahshomar-indicator", 'org.gahshomar.Gahshomar-no-icon',
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS)

        # hook status (active state) to settings. The settings object needs to
        # be kept around.
        self.settings = Gio.Settings.new('org.gahshomar.Gahshomar')
        self.settings.connect('changed::appindicator', self.should_activate)
        # you need to read the key at least once after connecting to the signal
        self.should_activate(self.settings, 'appindicator')

        self.menu_setup()

        self.calendar.connect("notify::date", self.update)
        self.calendar.connect("notify::date-format", self.update)
        self.update(self.calendar)

    def __del__(self):
        self.ind.set_status(AppIndicator3.IndicatorStatus.PASSIVE)

    def should_activate(self, settings, key):
        appindicator = settings.get_boolean(key)
        logger.debug("AppIndicator Enabled: %s", appindicator)
        if appindicator:
            self.ind.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        else:
            self.ind.set_status(AppIndicator3.IndicatorStatus.PASSIVE)

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

    def update(self, calendar, *args):
        self.today_item.set_label(calendar.full_date)
        self.ind.set_label(calendar.day_str, '29')

    def activate(self, *args):
        self.application.do_activate()

    def quit(self, widget):
        self.application.quit()
