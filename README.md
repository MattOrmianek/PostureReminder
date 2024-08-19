# Posture Reminder

This Python script creates a macOS status bar menu application that provides a simple interface to manage a popup reminder system. The application features a timer interval slider, a mode selection dropdown, and a toggle button to enable or disable the popup reminders.

## Features
Timer Interval Slider: Allows the user to adjust the time interval between popup reminders. The interval can be set between 5 and 300 seconds.
Mode Selection Dropdown: Offers three modes for popup positioning:
Custom: (Currently behaves like "Center") - Intended for future customization.
Random: Randomly positions the popup on the screen.
Center: Positions the popup at the center of the screen.
Enable/Disable Popup Toggle: Allows the user to enable or disable the popup reminders directly from the status bar menu.
Popup Reminder: A simple popup that reminds the user to check their posture. The popup is always on top and closes automatically after 1.5 seconds.

## Compile
```bash
python setup.py py2app -A
```

## Run
```bash
./dist/PostureReminder.app/Contents/MacOS/PostureReminder
```