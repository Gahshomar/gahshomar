from gi.repository import GObject
import datetime

class Date(GObject.GObject):
    """The class for representing dates in Gahshomar
    """
    __gtype_name__ = 'GahshomarDate'

    def __init__(self, date=None, **kwargs):
        self._date = date
        super().__init__(**kwargs)

    @GObject.Property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

# define today
TODAY = Date(datetime.date.today())
"""This object represents today in Gahshomar.
You can connect to its signal to see if today has changed:
``TODAY.connect("notify::date", on_today_changed)``
"""

SELECTED_DATE = Date(datetime.date.today())
"""This object represents the current selected date in Gahshomar's interface.
You can connect to its signal to see if selected date has changed:
``SELECTED_DATE.connect("notify::date", on_date_changed)``
"""
