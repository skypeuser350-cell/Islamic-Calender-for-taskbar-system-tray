import pystray
from PIL import Image, ImageDraw
from hijridate import Gregorian, Hijri
import tkinter as tk
from tkinter import messagebox
import threading
import os
import sys

class IslamicCalendarTray:
    def __init__(self):
        self.offset = -1  # Default set to -1 for Indian Hijri Calendar
        self.icon = None
        self.create_tray_icon()

    def get_date_string(self):
        """Calculates Hijri date using today's Gregorian date and manual offset, formatted as '1st Ramadan 1447 H'."""
        h_today = Gregorian.today().to_hijri()
        
        # Create a new Hijri date object with the offset applied to handle month/year changes automatically
        try:
            # We must convert back to a manipulatable date object
            h_adjusted = Hijri(h_today.year, h_today.month, h_today.day + self.offset)
        except ValueError:
            # Fallback for edge cases if direct manipulation fails
            g_today = Gregorian.today()
            g_adjusted = g_today.replace(day=g_today.day + self.offset)
            h_adjusted = g_adjusted.to_hijri()

        day = h_adjusted.day
        month_name = h_adjusted.month_name()
        year = h_adjusted.year
        
        # Helper function to get ordinal suffix (1st, 2nd, 3rd, 4th...)
        def ordinal(n):
            if 11 <= (n % 100) <= 13:
                suffix = 'th'
            else:
                suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
            return f"{n}{suffix}"

        return f"{ordinal(day)} {month_name} {year} H"

    def create_icon_image(self):
        """Loads your custom icon.png file or uses a fallback."""
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        
        icon_path = os.path.join(base_path, "icon.png")
        
        try:
            return Image.open(icon_path)
        except Exception:
            # Fallback to a plain green box if your image is missing
            return Image.new('RGB', (64, 64), color=(0, 128, 0))

    def show_info(self):
        """Opens a simple GUI popup to show the current Hijri date."""
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        messagebox.showinfo("Islamic Calendar", f"Current Hijri Date:\n{self.get_date_string()}")
        root.destroy()

    def set_offset(self, val):
        """Updates the offset and refreshes the tray icon tooltip."""
        self.offset = val
        if self.icon:
            # Update the tooltip title text with the new format
            self.icon.title = f"Hijri: {self.get_date_string()}"

    def create_tray_icon(self):
        """Initializes the pystray menu and icon."""
        menu = pystray.Menu(
            pystray.MenuItem("View Full Date", self.show_info),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Indian (-1 Day)", lambda: self.set_offset(-1), checked=lambda item: self.offset == -1),
            pystray.MenuItem("Standard (0 Days)", lambda: self.set_offset(0), checked=lambda item: self.offset == 0),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", lambda: self.icon.stop())
        )
        
        self.icon = pystray.Icon(
            "IslamicCalendar", 
            self.create_icon_image(), 
            # Set the initial tooltip title with the new format
            title=f"Hijri: {self.get_date_string()}", 
            menu=menu
        )

    def run(self):
        """Starts the tray application."""
        self.icon.run()

if __name__ == "__main__":
    app = IslamicCalendarTray()
    app.run()
