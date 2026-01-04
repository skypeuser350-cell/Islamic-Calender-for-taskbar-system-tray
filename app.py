import pystray
from PIL import Image, ImageDraw
from hijridate import Gregorian
import tkinter as tk
from tkinter import messagebox

class IslamicCalendarTray:
    def __init__(self):
        self.offset = -1  # Default set to -1 for Indian Hijri Calendar
        self.icon = None
        self.update_tray()

    def get_date_string(self):
        # Calculate Hijri date with manual offset
        h = Gregorian.today().to_hijri()
        return f"{h.year}-{h.month}-{h.day + self.offset} AH"

    def create_icon_image(self):
        # Creates a green square icon with a crescent symbol
        img = Image.new('RGB', (64, 64), color=(0, 128, 0))
        d = ImageDraw.Draw(img)
        d.text((15, 15), "🌙", fill=(255, 255, 255))
        return img

    def show_info(self):
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Islamic Calendar", f"Current Hijri Date: {self.get_date_string()}")
        root.destroy()

    def set_offset(self, val):
        self.offset = val
        self.icon.title = f"Hijri: {self.get_date_string()}"

    def run(self):
        menu = pystray.Menu(
            pystray.MenuItem("View Date", self.show_info),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Indian (-1 Day)", lambda: self.set_offset(-1), checked=lambda item: self.offset == -1),
            pystray.MenuItem("Standard (0 Days)", lambda: self.set_offset(0), checked=lambda item: self.offset == 0),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", lambda: self.icon.stop())
        )
        self.icon = pystray.Icon("IslamicCalendar", self.create_icon_image(), 
                                 title=f"Hijri: {self.get_date_string()}", menu=menu)
        self.icon.run()

if __name__ == "__main__":
    IslamicCalendarTray().run()
