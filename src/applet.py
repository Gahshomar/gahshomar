from gettext import gettext as _
from gi.repository import Gtk, Gio
import logging
logger = logging.getLogger(__name__)


class Applet(object):
    """Gahshomar's appindicator"""

    def __init__(self, name, settings_key, application, calendar, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.settings_key = settings_key
        self.application = application
        self.calendar = calendar

        # hook status (active state) to settings. The settings object needs to
        # be kept around.
        self.settings = Gio.Settings.new('org.gahshomar.Gahshomar')
        self.settings.connect(
            'changed::' + self.settings_key, self.should_activate)
        # you need to read the key at least once after connecting to the signal
        self.should_activate(self.settings, self.settings_key)

        self.menu_setup()

        self.calendar.connect("notify::date", self.update)
        self.calendar.connect("notify::date-format", self.update)
        self.update(self.calendar)

    def __del__(self):
        self.do_deactivate()

    def should_activate(self, settings, key):
        applet = settings.get_boolean(key)
        logger.debug("%s enabled: %s", self.name, applet)
        if applet:
            self.do_activate()
        else:
            self.do_deactivate()

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
        self.menu.show_all()

    def update(self, calendar, *args):
        self.today_item.set_label(calendar.full_date)

    def activate(self, *args):
        self.application.do_activate()

    def quit(self, widget):
        self.application.quit()
