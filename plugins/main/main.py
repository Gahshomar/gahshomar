from os.path import abspath, join
import sys
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from gi.repository import GObject, Peas, Gtk, Gio, GLib, Gdk

try:
    import gahshomar
except ImportError:
    gahshomar = None


class MainPlugin(GObject.Object, Peas.Activatable):
    __gtype_name__ = 'MainPlugin'

    object = GObject.property(type=GObject.Object)

    def do_activate(self):
        global gahshomar
        if gahshomar is None:
            self.info = Peas.Engine.get_plugin_info(Peas.Engine.get_default(),
                                                    'main')
            sys.path.insert(0, abspath(join(self.info.get_module_dir(), '..')))
        from gahshomar.application import EventsHandler
        from gahshomar.window import Window
        self.object._window = None
        self.object.setting_win = None
        self.object.handler = EventsHandler()
        if not self.object._window:
            self.object._window = Window(self.object)
            self.object.add_window(self.object._window)
        else:
            self.object._window.present()

        self.object.preferencesAction = Gio.SimpleAction.new('preferences',
                                                             None)
        self.object.preferencesAction.connect('activate', self.preferences)
        self.object.add_action(self.object.preferencesAction)

        self.object.aboutAction = Gio.SimpleAction.new('about', None)
        self.object.aboutAction.connect('activate', self.about)
        self.add_action(self.object.aboutAction)

        self.object.helpAction = Gio.SimpleAction.new('help', None)
        self.object.helpAction.connect('activate', self.help)
        self.add_action(self.object.helpAction)

        self.settings = Gio.Settings.new('org.gahshomar.Gahshomar')
        try:
            self.date_format = str(
                self.settings.get_value('persian-date-format'))
            self.date_format = self.date_format.replace("'", "")
        except Exception:
            logger.exception(Exception)
            self.date_format = '%A، %d %B %Y'
        self.load_plugins()
        self.connect_plugin_signals()

    def do_deactivate(self):
        self.object.remove_window(self.object._window)
        self.disconnect_plugin_signals()

    def do_update_state(self):
        self.object.handler.update_everything()

    def preferences(self, action=None, param=None):
        from gahshomar.settings_page import SettingsWindow
        self.object.setting_win = SettingsWindow(self)
        self.object.setting_win.set_transient_for(self.object._window)
        self.object.setting_win.show()

    def help(self, action, param):
        Gtk.show_uri(None, "help:gahshomar", Gdk.CURRENT_TIME)
        return 'help activated!'

    def about(self, action, param):
        builder = Gtk.Builder()
        builder.add_from_resource('/org/gahshomar/Gahshomar/AboutDialog.ui')
        about = builder.get_object('about_dialog')
        about.set_transient_for(self._window)
        about.connect("response", self.about_response)
        about.show()

    def load_plugins(self):
        engine = Peas.Engine.get_default()
        crashed = bool(self.settings.get_value('app-crashed'))
        names = str(self.settings.get_value('enabled-plugins')).replace("'", "")
        names = names.split(';')
        if '' in names:
            names.remove('')
        if crashed:
            if names:
                logging.warn('Disabling all the plugins since '
                             'the app crashed last time!')
                warnmsg = Gtk.MessageDialog(
                    text='Disabling all the plugins since the app crashed last '
                         'time!',
                    message_type=Gtk.MessageType.WARNING,
                    buttons=Gtk.ButtonsType.CLOSE,
                    transient_for=self.object._window)
                warnmsg.run()
                warnmsg.destroy()
            self.settings.set_value('enabled-plugins',
                                    GLib.Variant('s', ''))
            self.settings.set_value('app-crashed',
                                    GLib.Variant.new_boolean(False))
            return

        self.settings.set_value('app-crashed',
                                GLib.Variant.new_boolean(True))
        for name in names:
            info = engine.get_plugin_info(name)
            if info is not None:
                engine.load_plugin(info)

    def connect_plugin_signals(self):
        engine = Peas.Engine.get_default()
        self.id_load = engine.connect_after('load-plugin',
                                            self.plugin_loaded, None)
        self.id_unload = engine.connect_after('unload-plugin',
                                              self.plugin_unloaded, None)

    def disconnect_plugin_signals(self):
        engine = Peas.Engine.get_default()
        engine.disconnect(self.id_load)
        engine.disconnect(self.id_unload)

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

    def do_get_day(self):
        from gahshomar.khayyam import JalaliDate
        day = JalaliDate.today().strftime('%d')
        if day[0] == '۰':
            day = day[1:]
        return day

    def do_get_date(self):
        from gahshomar.khayyam import JalaliDate
        return JalaliDate.today().strftime(self.date_format)


# class MainConfigurable(GObject.Object, PeasGtk.Configurable):
#     __gtype_name__ = 'MainConfigurable'

#     def do_create_configure_widget(self):
#         return Gtk.Label.new("Main plugin configure widget")
