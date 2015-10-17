import datetime
from gettext import gettext as _
import logging
logger = logging.getLogger(__name__)

from gi.repository import GObject, Peas, Gtk, Gio, GLib
# , Gdk
# import cairo

from gahshomar import log, calendar
import gahshomar.khayyam as khayyam


class StatusIconPlugin(GObject.Object, Peas.Activatable):
    __gtype_name__ = 'StatusIconPlugin'

    object = GObject.property(type=GObject.Object)

    @log
    def do_activate(self):
        self.statusicon = Gtk.StatusIcon(title='gahshomar',
                                         has_tooltip=True, visible=True)
        self.statusicon.connect('activate', self.activate)
        self.statusicon.connect('popup-menu', self.right_click_event)

        self.date = datetime.date.today()
        self.app = self.object

        self.settings = Gio.Settings.new('org.gahshomar.Gahshomar')
        self.date_format = str(self.settings.get_value('persian-date-format'))
        self.date_format = self.date_format.replace("'", "")

        self.window = Gtk.OffscreenWindow(app_paintable=True)
        self.window.screen = self.window.get_screen()
        self.window.visual = self.window.screen.get_rgba_visual()
        if self.window.visual is not None and \
           self.window.screen.is_composited():
            self.window.set_visual(self.window.visual)
        self.day_label = Gtk.Label('00')
        self.window.add(self.day_label)
        self.window.connect("damage-event", self.draw_complete_event)
        self.window.connect('draw', self.draw)
        self.window.show_all()
        # self.pixbuf = Gtk.IconTheme.load_icon(
        #     Gtk.IconTheme(), 'gahshomar', 24, Gtk.IconLookupFlags.NO_SVG)

        self.menu_setup()
        self.update()

        self.timer_id = GLib.timeout_add_seconds(5, self.update)

    @log
    def draw_complete_event(self, window, event):
        self.statusicon.set_from_pixbuf(window.get_pixbuf())

    @log
    def right_click_event(self, statusicon, button, activate_time):
        self.menu.popup(None, None, None, None, button, activate_time)

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
        self.menu.show_all()

    @log
    def get_date_formatted(self, frmt=None):
        if frmt is None:
            frmt = self.date_format
        text = calendar.glib_strftime(frmt,
                                      khayyam.JalaliDate.from_date(self.date))
        if text[0] == '0' or text[0] == '۰':
            text = text[1:]
        return text

    @log
    def quit(self, widget):
        self.app.quit()

    @log
    def update(self):
        self.date = datetime.date.today()
        date_formatted = self.get_date_formatted()
        self.statusicon.set_tooltip_text(date_formatted)
        self.today_item.set_label(date_formatted)
        day = self.get_date_formatted(_('%d'))
        # pixbuf = self.put_text(self.pixbuf, str(int(day)), 7, 3)
        # self.statusicon.set_from_pixbuf(pixbuf)

        day = '<span fgcolor="#bebebe">{}</span>'.format(day)
        self.day_label.set_markup(day)

        # make sure to return True so that it keeps updating
        return True

    @log
    def activate(self, *args):
        self.app.do_activate(self.app)

    @log
    def do_deactivate(self):
        self.statusicon.set_visible(False)
        GLib.source_remove(self.timer_id)

    @log
    def do_update_state(self):
        self.update()

    @log
    def draw(self, widget, cr, userdata=None):
        cr.set_source_rgba(1, 1, 1, 0)
        cr.set_operator(1)
        cr.paint()
        cr.set_operator(2)
        return False

    # def put_text(self, pixbuf, text, x, y):
    #     surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, pixbuf.get_width(),
    #         pixbuf.get_height())
    #     context = cairo.Context(surface)

    #     Gdk.cairo_set_source_pixbuf(context, pixbuf, 0, 0)
    #     context.paint() #paint the pixbuf

    #     #add the text
    #     fontsize= 18
    #     context.move_to(x, y+fontsize)
    #     context.set_font_size(fontsize)
    #     context.set_source_rgba(46/255,52/255,54/255,1)
    #     context.show_text(text)

    #     #get the resulting pixbuf
    #     surface= context.get_target()
    #     pixbuf= Gdk.pixbuf_get_from_surface(surface, 0, 0,
    #         surface.get_width(), surface.get_height())

    #     return pixbuf
