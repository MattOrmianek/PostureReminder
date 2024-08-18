import objc
from Cocoa import (
    NSApplication, NSApp, NSWindow, NSWindowStyleMask,
    NSRunningApplication, NSApplicationActivationPolicyRegular,
    NSTimer, NSImage, NSStatusBar, NSMenu, NSMenuItem, NSSlider,
    NSTextField, NSScreen, NSFont, NSWindowStyleMaskTitled,
    NSWindowStyleMaskClosable, NSTextAlignmentCenter, NSView
)
from Foundation import NSObject, NSMakeRect
import random
import sys

class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        self.timer_interval = 10
        self.create_menu_bar()
        self.start_timer()
        self.active_status = True

    def create_menu_bar(self):
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
            slider_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Timer Interval", None, "")

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
            self.slider_value_label = NSTextField.alloc().initWithFrame_(NSMakeRect(210, -10, 40, 30))
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

            # Toggle item to enable/disable the popup
            self.toggle_popup_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Disable Popup", "togglePopup:", "")
            self.toggle_popup_item.setTarget_(self)
            self.toggle_popup_item.setAction_("togglePopupStatus:")
            self.menu.addItem_(self.toggle_popup_item)

            # Quit item
            quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Quit", "terminate:", "")
            self.menu.addItem_(quit_item)

            # Set the menu
            self.status_item.setMenu_(self.menu)
        except Exception as error:
            print(error)

    def updateTimerInterval_(self, sender):
        self.timer_interval = sender.floatValue()
        self.slider_value_label.setStringValue_(str(int(self.timer_interval)))  # Update the label with the new value
        self.start_timer()

    def togglePopupStatus_(self, sender):
        self.active_status = not self.active_status
        if self.active_status:
            self.toggle_popup_item.setTitle_("Disable Popup")
        else:
            self.toggle_popup_item.setTitle_("Enable Popup")

    def start_timer(self):
        if hasattr(self, 'timer'):
            self.timer.invalidate()

        self.timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            self.timer_interval, self, "showPopup:", None, True
        )

    def showPopup_(self, timer):
        try:
            if self.active_status:
                screen_width = NSScreen.mainScreen().frame().size.width
                screen_height = NSScreen.mainScreen().frame().size.height

                window_width, window_height = 300, 100
                x = random.randint(0, int(screen_width - window_width))
                y = random.randint(0, int(screen_height - window_height))

                window_style = NSWindowStyleMaskTitled | NSWindowStyleMaskClosable

                self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
                    NSMakeRect(x, y, window_width, window_height),
                    window_style,
                    2,
                    False
                )
                self.window.setTitle_("")
                self.window.setLevel_(3)  # Always on top
                self.window.setContentView_(NSApplication.sharedApplication().delegate().create_label())
                self.window.makeKeyAndOrderFront_(None)

                # Schedule the window to close after 5 seconds
                NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
                    1.5, self, "closePopup:", None, False
                )

                print("Popup window created at position:", x, y)
        except Exception as error:
            print(error)

    def create_label(self):
        label = NSTextField.alloc().initWithFrame_(NSMakeRect(10, 10, 280, 80))
        label.setStringValue_("Check your posture!")
        label.setEditable_(False)
        label.setBezeled_(False)
        label.setDrawsBackground_(False)
        label.setFont_(NSFont.systemFontOfSize_(40))
        label.setAlignment_(NSTextAlignmentCenter)  # Center the text horizontall
        return label

    def closePopup_(self, timer):
        self.window.orderOut_(None)
        self.window = None
        print("Popup window closed")

if __name__ == "__main__":
    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    app.setDelegate_(delegate)
    app.setActivationPolicy_(NSApplicationActivationPolicyRegular)
    NSRunningApplication.currentApplication().activateWithOptions_(2)
    app.run()
