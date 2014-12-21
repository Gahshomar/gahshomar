from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManagerSingleton


class ConfirmQuit(IPlugin):
    """
    Confirm Quit Plugin

    Connects to the window's "delete-event" signal to confirm the user before
    exiting the applicaiton.

    Note: In a real world application, you would likely create a base plugin
    class derived from `IPlugin` rather than extending `IPlugin` directly.
    """
    def __init__(self):
        # Make sure to call the parent class (`IPlugin`) methods when
        # overriding them.
        super().__init__()

        # The `app` property was added to the manager singleton instance when
        # the manager was setup. See ExampleApp.__init__() in the
        # yapsy-gtk-example.py file.
        manager = PluginManagerSingleton.get()
        self.parent = manager.parent

    def activate(self):
        # Make sure to call `activate()` on the parent class to ensure that the
        # `is_activated` property gets set.
        super().activate()

        # Connect to the "delete-event" and store the handler_id so that the
        # signal handler can be disconnected when the plugin is deactivated.
        # If your plugin connects to multiple signals on multiple objects then
        # you'll want to store the object and the handler_id of each of those.
        # self._handler = self.parent.connect("delete-event",
        #                                     self.parent.toggle_main_win)
        self.xdg_current_desktop = self.parent.xdg_current_desktop
        self.parent.xdg_current_desktop = 'unity'
        self.parent.toggle_main_win()
        self.parent.set_titlebar(None)
        self.parent.draw_interface()
        self.parent.setup_header_bar()
        self.parent.toggle_main_win()
        try:
            self.parent.dialog.present()
        except Exception:
            pass

    def deactivate(self):
        # Make sure to call `deactivate()` on the parent class to ensure that
        # the `is_activated` property gets set.
        super().deactivate()

        # Need to disconnect the signal handler when the plugin is deactivated.
        # self.parent.disconnect(self._handler)
        self.parent.xdg_current_desktop = self.xdg_current_desktop
        self.parent.toggle_main_win()
        self.parent.draw_interface()
        self.parent.setup_header_bar()
        self.parent.toggle_main_win()
        try:
            self.parent.dialog.present()
        except Exception:
            pass

    # def _on_window_delete_event(self, window, event, data=None):
    #     """
    #     Show a message dialog prompting the user to confirm that they want to
    #     quit. Return True if they answer "No" to stop the event from
    #     propogating and return False if they answer "Yes" to allow the event
    #     to occur.
    #     """
    #     dialog = Gtk.MessageDialog(window, Gtk.DialogFlags.MODAL |
    #                                Gtk.DialogFlags.DESTROY_WITH_PARENT,
    #                                Gtk.MessageType.QUESTION,
    #                                Gtk.ButtonsType.YES_NO,
    #                                "Are you sure you want to quit?")
    #     dialog.set_title("Confirm quit")
    #     r = dialog.run()
    #     dialog.destroy()

    #     if r == Gtk.ResponseType.YES:
    #         return False
    #     else:
    #         return True
