import pystray
from PIL import Image, ImageDraw
from hijridate import Gregorian
import tkinter as tk
from tkinter import messagebox
import threading

class IslamicCalendarTray:
    def __init__(self):
        # Default set to -1 for Indian Hijri Calendar (Current Date: Jan 4, 2026)
        self.offset = -1  
        self.icon = None
        # We start the icon setup here
        self.create_tray_icon()

    def get_date_string(self):
        """Calculates Hijri date using today's Gregorian date and manual offset."""
        h = Gregorian.today().to_hijri()
        # Adjust day based on regional sighting offset
        adjusted_day = h.day + self.offset
        return f"{h.year}-{h.month}-{adjusted_day} AH"

    def create_icon_image(self):
        """Creates a green 64x64 icon with a moon symbol for the tray."""
        img = Image.new('RGB', (64, 64), color=(0, 128, 0))
        d = ImageDraw.Draw(img)
        # Using a simple text-based moon icon for compatibility
        d.text((20, 20), "🌙", fill=(255, 255, 255))
        return img

    def show_info(self):
        """Opens a simple GUI popup to show the current Hijri date."""
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True) # Keep it on top of other windows
        messagebox.showinfo("Islamic Calendar", f"Current Hijri Date: {self.get_date_string()}")
        root.destroy()

    def set_offset(self, val):
        """Updates the offset and refreshes the tray icon tooltip."""
        self.offset = val
        if self.icon:
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
            title=f"Hijri: {self.get_date_string()}", 
            menu=menu
        )

    def run(self):
        """Starts the tray application."""
        self.icon.run()

if __name__ == "__main__":
    app = IslamicCalendarTray()
    app.run()
