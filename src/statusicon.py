from .applet import Applet
from gi.repository import Gtk
import logging
logger = logging.getLogger(__name__)


class StatusIcon(Applet):
    """Gahshomar's status icon"""

    def __init__(self, application, calendar, **kwargs):
        # setup the StatusIcon
        self.statusicon = Gtk.StatusIcon(title='gahshomar',
                                         has_tooltip=True, visible=True)
        self.statusicon.connect('activate', self.activate)
        self.statusicon.connect('popup-menu', self.right_click_event)

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

        super().__init__(
            'StatusIcon', 'statusicon', application, calendar, **kwargs)

    def do_activate(self):
        self.statusicon.set_visible(True)

    def do_deactivate(self):
        self.statusicon.set_visible(False)

    def update(self, calendar, *args):
        super().update(calendar, *args)
        date_formatted = self.calendar.full_date
        self.statusicon.set_tooltip_text(date_formatted)
        day = '<span fgcolor="#bebebe">{}</span>'.format(self.calendar.day_str)
        self.day_label.set_markup(day)

    def draw_complete_event(self, window, event):
        self.statusicon.set_from_pixbuf(window.get_pixbuf())

    def right_click_event(self, statusicon, button, activate_time):
        self.menu.popup(None, None, None, None, button, activate_time)

    def draw(self, widget, cr, userdata=None):
        cr.set_source_rgba(1, 1, 1, 0)
        cr.set_operator(1)
        cr.paint()
        cr.set_operator(2)
        return False
