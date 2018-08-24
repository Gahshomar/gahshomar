# -*- Mode: Python; coding: utf-8; indent-tabs-mode: s; tab-width: 4 -*-

from gi.repository import Gtk, Gio
from .gi_composites import GtkTemplate
import logging
logger = logging.getLogger(__name__)


@GtkTemplate(ui='/org/gahshomar/Gahshomar/preferences.ui')
class GahshomarPreferences(Gtk.Dialog):
    __gtype_name__ = 'GahshomarPreferences'

    afghan_month_switch = GtkTemplate.Child()
    appindicator_switch = GtkTemplate.Child()
    statusicon_switch = GtkTemplate.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()

        # bind the afghan-month setting to its switch
        self.settings = Gio.Settings.new('org.gahshomar.Gahshomar')
        self.settings.bind("afghan-month", self.afghan_month_switch, "active",
                           Gio.SettingsBindFlags.DEFAULT)

        # bind the appindicator setting to its switch
        self.settings = Gio.Settings.new('org.gahshomar.Gahshomar')
        self.settings.bind("appindicator", self.appindicator_switch, "active",
                           Gio.SettingsBindFlags.DEFAULT)

        # bind the statusicon setting to its switch
        self.settings = Gio.Settings.new('org.gahshomar.Gahshomar')
        self.settings.bind("statusicon", self.statusicon_switch, "active",
                           Gio.SettingsBindFlags.DEFAULT)
