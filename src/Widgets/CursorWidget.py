from textual.widget import Widget
from Services.EditorService import EditorService

class CursorWidget(Widget):
    """ Class housing the (visible) cursor widget"""

    def __init__(self):
        super().__init__(id="cursor")
        self.on = True
        self.timer = None

    def on_mount(self):
        self.timer = self.set_interval(0.5, self.toggle)

    def toggle(self):
        """ Toggles cursor's visibility """

        self.on = not self.on

        if self.on:
            self.styles.display="block"
        else:
            self.styles.display="none"

    def pause_blink(self):
        """ Stops cursor blinking for 1.0s """

        self.on = True
        self.styles.display="block"

        if self.timer:
            self.timer.pause()

        self.set_timer(1.0, self.restart_blink)

    def restart_blink(self):
        """ Resumes cursor blinking """
        if self.timer:
            self.timer.resume()

