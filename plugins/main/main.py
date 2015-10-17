from os.path import abspath, join
import sys
import gettext
gettext.bindtextdomain('gahshomar')
gettext.textdomain('gahshomar')
_ = gettext.gettext
from gi.repository import GObject, Peas, Gtk, Gio, GLib, Gdk

settings = Gio.Settings.new('org.gahshomar.Gahshomar')
verbose = bool(settings.get_value('verbose'))

import logging
if verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    import gahshomar
    from gahshomar import log, calendar
except ImportError:
    gahshomar = None
    log = lambda x: x


class EventsHandler(object):
    """docstring for EventsHandler"""
    @log
    def __init__(self):
        super().__init__()
        self.updateables = list()

    @log
    def update_everything(self, **kwargs):
        for instance in self.updateables:
            instance.update(**kwargs)


class MainPlugin(GObject.Object, Peas.Activatable):
    __gtype_name__ = 'MainPlugin'

    object = GObject.property(type=GObject.Object)

    @log
    def do_activate(self):
        global gahshomar
        if gahshomar is None:
            self.info = Peas.Engine.get_plugin_info(Peas.Engine.get_default(),
                                                    'main')
            sys.path.insert(0, abspath(join(self.info.get_module_dir(),
                                            '..',
                                            '..')))
        from gahshomar.window import Window
        self.object.handler = EventsHandler()
        self.object._window = Window(self.object)

        self.object.preferencesAction = Gio.SimpleAction.new('preferences',
                                                             None)
        self.object.preferencesAction.connect('activate', self.preferences)
        self.object.add_action(self.object.preferencesAction)

        self.object.aboutAction = Gio.SimpleAction.new('about', None)
        self.object.aboutAction.connect('activate', self.about)
        self.object.add_action(self.object.aboutAction)

        self.object.helpAction = Gio.SimpleAction.new('help', None)
        self.object.helpAction.connect('activate', self.help)
        self.object.add_action(self.object.helpAction)

        self.settings = Gio.Settings.new('org.gahshomar.Gahshomar')
        try:
            self.date_format = str(
                self.settings.get_value('persian-date-format'))
            self.date_format = self.date_format.replace("'", "")
        except Exception:
            logger.exception(Exception)
            self.date_format = _('%A، %d %B %Y')
        self.load_plugins()
        self.connect_plugin_signals()

    @log
    def do_deactivate(self):
        self.object.remove_window(self.object._window)
        self.disconnect_plugin_signals()

    @log
    def do_update_state(self):
        self.object.handler.update_everything()

    @log
    def preferences(self, action=None, param=None):
        from gahshomar.settings_page import SettingsWindow
        self.object.setting_win = SettingsWindow(self.object)
        self.object.setting_win.set_transient_for(self.object._window)
        self.object.setting_win.show()

    @log
    def help(self, action, param):
        Gtk.show_uri(None, "help:gahshomar", Gdk.CURRENT_TIME)
        return 'help activated!'

    @log
    def about(self, action, param):
        builder = Gtk.Builder()
        builder.add_from_resource('/org/gahshomar/Gahshomar/AboutDialog.ui')
        about = builder.get_object('about_dialog')
        about.set_transient_for(self.object._window)
        about.connect("response", self.about_response)
        about.show()

    @log
    def about_response(self, dialog, response):
        dialog.destroy()

    @log
    def load_plugins(self):
        engine = Peas.Engine.get_default()
        # crashed = bool(self.settings.get_value('app-crashed'))
        names = str(self.settings.get_value('enabled-plugins')).replace("'", "")
        names = names.split(';')
        if '' in names:
            names.remove('')
        # if crashed:
        #     if names:
        #         logging.warn(_('Disabling all the plugins since '
        #                        'the app crashed last time!'))
        #         warnmsg = Gtk.MessageDialog(
        #             text=_('Disabling all the plugins since the app crashed '
        #                    'last time!'),
        #             message_type=Gtk.MessageType.WARNING,
        #             buttons=Gtk.ButtonsType.CLOSE,
        #             transient_for=self.object._window)
        #         warnmsg.run()
        #         warnmsg.destroy()
        #     self.settings.set_value('enabled-plugins',
        #                             GLib.Variant('s', ''))
        #     self.settings.set_value('app-crashed',
        #                             GLib.Variant.new_boolean(False))
        #     return

        self.settings.set_value('app-crashed',
                                GLib.Variant.new_boolean(True))
        for name in names:
            info = engine.get_plugin_info(name)
            if info is not None:
                engine.load_plugin(info)

    @log
    def connect_plugin_signals(self):
        engine = Peas.Engine.get_default()
        self.id_load = engine.connect_after('load-plugin',
                                            self.plugin_loaded, None)
        self.id_unload = engine.connect_after('unload-plugin',
                                              self.plugin_unloaded, None)

    @log
    def disconnect_plugin_signals(self):
        engine = Peas.Engine.get_default()
        engine.disconnect(self.id_load)
        engine.disconnect(self.id_unload)

    @log
    def plugin_loaded(self, engine, plugin_info, data=None):
        name = plugin_info.get_module_name()
        if name == 'main':
            return
        if ';' in name:
            logging.warn('Unsupported plugin name. This plugin will not be kept'
                         ' enabled between sessions')
        names = str(self.settings.get_value('enabled-plugins')).replace("'", "")
        names = names.split(';')
        if '' in names:
            names.remove('')
        if name not in names:
            names.append(name)
            self.settings.set_value('enabled-plugins',
                                    GLib.Variant('s', ';'.join(names)))

    @log
    def plugin_unloaded(self, engine, plugin_info, data=None):
        name = plugin_info.get_module_name()
        if name == 'main':
            return
        names = str(self.settings.get_value('enabled-plugins')).replace("'", "")
        names = names.split(';')
        if '' in names:
            names.remove('')
        if name in names:
            names.remove(name)
            self.settings.set_value('enabled-plugins',
                                    GLib.Variant('s', ';'.join(names)))

    @log
    def do_get_day(self):
        from gahshomar.khayyam import JalaliDate
        day = calendar.glib_strftime(_('%d'), JalaliDate.today())
        if day[0] == '۰':
            day = day[1:]
        return day

    @log
    def do_get_date(self):
        from gahshomar.khayyam import JalaliDate
        return calendar.glib_strftime(self.date_format, JalaliDate.today())


# class MainConfigurable(GObject.Object, PeasGtk.Configurable):
#     __gtype_name__ = 'MainConfigurable'

#     @log
#     def do_create_configure_widget(self):
#         return Gtk.Label.new("Main plugin configure widget")
