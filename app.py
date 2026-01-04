import pystray
from PIL import Image, ImageDraw
from hijridate import Gregorian, Hijri
import tkinter as tk
from tkinter import messagebox
import threading
import os
import sys
import requests # Import the requests library
import datetime

class IslamicCalendarTray:
    def __init__(self):
        self.offset = -1  # Default set to -1 for Indian Hijri Calendar
        self.icon = None
        self.daily_quote = "Fetching daily verse..."
        self.last_fetch_date = None
        self.create_tray_icon()
        self.fetch_daily_quote() # Initial fetch

    def fetch_daily_quote(self):
        """Fetches a random Quranic verse using an API if the day has changed."""
        today = datetime.date.today()
        if self.last_fetch_date == today:
            return # Don't fetch the same quote multiple times a day

        self.last_fetch_date = today
        
        # API endpoint for a random verse with English translation (Pickthall)
        API_URL = "api.alquran.cloud"
        
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                data = response.json()
                ayah_text = data['data']
                surah_name = data['data']['surah']['englishName']
                ayah_number = data['data']['numberInSurah']
                self.daily_quote = f"Quran ({surah_name}:{ayah_number}):\n\"{ayah_text}\""
            else:
                self.daily_quote = "Failed to fetch daily verse from API."
        except requests.exceptions.RequestException:
            self.daily_quote = "Error: Could not connect to the internet to fetch quote."

    def get_date_string(self):
        # ... [Ordinal logic remains the same as previous script] ...
        h_today = Gregorian.today().to_hijri()
        try:
            h_adjusted = Hijri(h_today.year, h_today.month, h_today.day + self.offset)
        except ValueError:
            g_today = Gregorian.today()
            g_adjusted = g_today.replace(day=g_today.day + self.offset)
            h_adjusted = g_adjusted.to_hijri()

        day = h_adjusted.day
        month_name = h_adjusted.month_name()
        year = h_adjusted.year
        
        def ordinal(n):
            if 11 <= (n % 100) <= 13:
                suffix = 'th'
            else:
                suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
            return f"{n}{suffix}"

        return f"{ordinal(day)} {month_name} {year} H"

    def create_icon_image(self):
        # ... [Icon logic remains the same] ...
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        
        icon_path = os.path.join(base_path, "icon.png")
        
        try:
            return Image.open(icon_path)
        except Exception:
            return Image.new('RGB', (64, 64), color=(0, 128, 0))

    def show_info(self):
        """Opens a GUI popup with date AND the daily quote."""
        # Refresh the quote just in case an API call failed earlier
        self.fetch_daily_quote() 
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        # Combine date and quote in the message box
        full_message = f"Current Hijri Date:\n{self.get_date_string()}\n\n---\n\n{self.daily_quote}"
        messagebox.showinfo("Islamic Calendar & Daily Verse", full_message)
        root.destroy()

    def set_offset(self, val):
        self.offset = val
        if self.icon:
            self.icon.title = f"Hijri: {self.get_date_string()}"

    def create_tray_icon(self):
        menu = pystray.Menu(
            pystray.MenuItem("View Full Date & Quote", self.show_info),
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
        self.icon.run()

if __name__ == "__main__":
    app = IslamicCalendarTray()
    app.run()
