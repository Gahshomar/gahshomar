from .applet import Applet
from gi.repository import AppIndicator3
import logging
logger = logging.getLogger(__name__)


class AppIndicator(Applet):
    """Gahshomar's appindicator"""

    def __init__(self, application, calendar, **kwargs):
        # setup the AppIndicator
        self.ind = AppIndicator3.Indicator.new(
            "Gahshomar-indicator", 'org.gahshomar.Gahshomar-no-icon',
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS)

        super().__init__(
            'AppIndicator', 'appindicator', application, calendar, **kwargs)

        self.ind.set_menu(self.menu)

    def do_activate(self):
        self.ind.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

    def do_deactivate(self):
        self.ind.set_status(AppIndicator3.IndicatorStatus.PASSIVE)

    def update(self, calendar, *args):
        super().update(calendar, *args)
        self.ind.set_label(calendar.day_str, '29')
