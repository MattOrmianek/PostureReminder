""" This is a simple Python script that creates a status bar menu with a slider and a toggle button.
    The slider allows you to adjust the time interval between the popups, and the toggle button
    enables/disables the popup.
"""

# pylint: disable=invalid-name, no-name-in-module, unused-argument, too-many-instance-attributes
# pylint: disable=broad-exception-caught, inconsistent-return-statements
import random
import logging
from Cocoa import (
    NSApplication,
    NSWindow,
    NSRunningApplication,
    NSApplicationActivationPolicyRegular,
    NSTimer,
    NSImage,
    NSStatusBar,
    NSMenu,
    NSMenuItem,
    NSSlider,
    NSTextField,
    NSScreen,
    NSFont,
    NSWindowStyleMaskTitled,
    NSWindowStyleMaskClosable,
    NSTextAlignmentCenter,
    NSView,
)
from Foundation import NSObject, NSMakeRect

console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s - %(filename)s:%(lineno)d - %(funcName)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
logger = logging.getLogger(__name__)


class AppDelegate(NSObject):
    """This is main class that creates the menu bar and handles the timer and popup window."""

    def __init__(self):
        self.timer_interval = None
        self.active_status = None
        self.window = None
        self.status_bar = None
        self.status_item = None
        self.menu = None
        self.toggle_popup_item = None
        self.slider_value_label = None
        self.timer = None
        self.mode = None

    def applicationDidFinishLaunching_(self, notification):
        """This method is called when the application is launched."""
        logging.info("Application launched")
        self.timer_interval = 10
        self.create_menu_bar()
        self.start_timer()
        self.active_status = True
        self.mode = "random"

    def create_menu_bar(self):
        """This method creates the menu bar and its items."""
        try:
            self.status_bar = NSStatusBar.systemStatusBar()
            self.status_item = self.status_bar.statusItemWithLength_(-1)
            icon = NSImage.imageNamed_("NSApplicationIcon")
            icon.setSize_((20, 20))
            self.status_item.button().setImage_(icon)
            self.menu = NSMenu.alloc().init()

            # Add space from the top of the menu
            self.menu.addItem_(NSMenuItem.separatorItem())
            # Slider for adjusting the timer interval
            slider_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                "Timer Interval", None, ""
            )

            # Container for slider and label
            container_view = NSView.alloc().initWithFrame_(NSMakeRect(0, 10, 250, 30))

            # Slider
            slider = NSSlider.alloc().initWithFrame_(NSMakeRect(10, -10, 200, 30))
            slider.setMinValue_(5)
            slider.setMaxValue_(300)
            slider.setFloatValue_(self.timer_interval)
            slider.setTarget_(self)
            slider.setAction_("updateTimerInterval:")

            # Label to display the current value of the slider
            self.slider_value_label = NSTextField.alloc().initWithFrame_(
                NSMakeRect(210, -10, 40, 30)
            )
            self.slider_value_label.setStringValue_(str(int(self.timer_interval)))
            self.slider_value_label.setEditable_(False)
            self.slider_value_label.setBezeled_(False)
            self.slider_value_label.setDrawsBackground_(False)
            self.slider_value_label.setAlignment_(NSTextAlignmentCenter)

            # Add slider and label to the container view
            container_view.addSubview_(slider)
            container_view.addSubview_(self.slider_value_label)

            # Set the container view to the menu item
            slider_item.setView_(container_view)
            self.menu.addItem_(slider_item)

            # Add Mode dropdown list
            mode_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                "Mode", None, ""
            )
            mode_menu = NSMenu.alloc().init()

            # Mode options
            modes = ["Custom", "Random", "Center"]
            for mode in modes:
                mode_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(mode, None, "")
                mode_item.setTarget_(self)
                mode_item.setAction_("selectMode:")
                mode_item.setRepresentedObject_(mode)
                mode_menu.addItem_(mode_item)

            mode_menu_item.setSubmenu_(mode_menu)
            self.menu.addItem_(mode_menu_item)

            # Toggle item to enable/disable the popup
            self.toggle_popup_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                "Disable Popup", "togglePopup:", ""
            )
            self.toggle_popup_item.setTarget_(self)
            self.toggle_popup_item.setAction_("togglePopupStatus:")
            self.menu.addItem_(self.toggle_popup_item)

            # Quit item
            quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                "Quit", "terminate:", ""
            )
            self.menu.addItem_(quit_item)

            # Set the menu
            self.status_item.setMenu_(self.menu)
        except Exception as error:
            logging.error("Error creating menu bar: %s", error)

    def selectMode_(self, sender):
        """Method to handle mode selection."""
        selected_mode = sender.representedObject()
        self.mode = selected_mode
        logging.info("Mode selected: %s", self.mode)

    def updateTimerInterval_(self, sender):
        """This method is called when the slider is adjusted."""
        try:
            self.timer_interval = sender.floatValue()
            self.slider_value_label.setStringValue_(
                str(int(self.timer_interval))
            )  # Update the label with the new value
            self.start_timer()
        except Exception as error:
            logging.error("Error updating timer interval: %s", error)

    def togglePopupStatus_(self, sender):
        """This method is called when the toggle button is clicked."""
        try:
            self.active_status = not self.active_status
            if self.active_status:
                self.toggle_popup_item.setTitle_("Disable Popup")
            else:
                self.toggle_popup_item.setTitle_("Enable Popup")
        except Exception as error:
            logging.error("Error toggling popup status: %s", error)

    def start_timer(self):
        """This method starts the timer."""
        try:
            if hasattr(self, "timer"):
                self.timer.invalidate()

            self.timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
                self.timer_interval, self, "showPopup:", None, True
            )
        except Exception as error:
            logging.error("Error starting timer: %s", error)

    def showPopup_(self, timer):
        """This method shows the popup window."""
        try:
            if self.active_status:
                screen_width = NSScreen.mainScreen().frame().size.width
                screen_height = NSScreen.mainScreen().frame().size.height

                window_width, window_height = 300, 100
                if self.mode == "Random":
                    x = random.randint(0, int(screen_width - window_width))
                    y = random.randint(0, int(screen_height - window_height))
                elif self.mode == "Center":
                    x = int(screen_width / 2 - window_width / 2)
                    y = int(screen_height / 2 - window_height / 2)
                elif self.mode == "Custom":
                    # TODO: add reading from config file what was saved by user, for now center
                    x = int(screen_width / 2 - window_width / 2)
                    y = int(screen_height / 2 - window_height / 2)
                else:
                    x = random.randint(0, int(screen_width - window_width))
                    y = random.randint(0, int(screen_height - window_height))

                window_style = NSWindowStyleMaskTitled | NSWindowStyleMaskClosable

                self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
                    NSMakeRect(x, y, window_width, window_height), window_style, 2, False
                )
                self.window.setTitle_("")
                self.window.setLevel_(3)  # Always on top
                self.window.setContentView_(
                    NSApplication.sharedApplication().delegate().create_label()
                )
                self.window.makeKeyAndOrderFront_(None)

                # Schedule the window to close after 5 seconds
                NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
                    1.5, self, "closePopup:", None, False
                )

                logging.info("Popup window created at position: %s, %s", x, y)
        except Exception as error:
            logging.error("Error showing popup: %s", error)

    def create_label(self):
        """This method creates the label for the popup window."""
        try:
            label = NSTextField.alloc().initWithFrame_(NSMakeRect(10, 10, 280, 80))
            label.setStringValue_("Check your posture!")
            label.setEditable_(False)
            label.setBezeled_(False)
            label.setDrawsBackground_(False)
            label.setFont_(NSFont.systemFontOfSize_(40))
            label.setAlignment_(NSTextAlignmentCenter)  # Center the text horizontall
            return label
        except Exception as error:
            logging.error("Error creating label: %s", error)

    def closePopup_(self, timer):
        """This method closes the popup window."""
        try:
            self.window.orderOut_(None)
            self.window = None
            logging.info("Popup window closed")
        except Exception as error:
            logging.error("Error closing popup: %s", error)


if __name__ == "__main__":
    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    app.setDelegate_(delegate)
    app.setActivationPolicy_(NSApplicationActivationPolicyRegular)
    NSRunningApplication.currentApplication().activateWithOptions_(2)
    app.run()
