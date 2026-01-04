# Islamic-Calender-for-taskbar-system-tray

A lightweight Windows application built with Python that displays the current Hijri date directly in your system tray (notification area), featuring a manual date offset for regional moon sighting variations (specifically the Indian calendar adjustment).
Features

🌙 System Tray Integration: Sits silently next to your clock, speaker, and Wi-Fi icons.

🗓️ Dynamic Date Display: Hover over the icon to see the current Hijri date.

🔧 Configurable Offset: Right-click the icon to manually adjust the date by -1 or +1 day to match local (e.g., Indian) sightings.

📦 Standalone EXE: Does not require Python to be installed on your computer.

🎟 Super Light weight : Yes on hardware below 1GB RAM it will stil run smoothly

--Installation & Download
Click on the releases button and then download the folder by scrolling down.

--How to Use
Run the EXE: The app starts minimized to the system tray (you might need to click the ^ arrow to see it).
View Date: Hover over the icon for a quick tooltip date.
Adjust Settings: Right-click the icon to bring up the menu. Select "Indian (-1 Day)" or "Standard (0 Days)" to adjust the calculation.
Run on Startup: To make the app run every time Windows starts, copy the .exe file shortcut into your Windows Startup folder (shell:startup).

--Technology Stack
Language: Python
Libraries: pystray, Pillow, hijridate, tkinter
Build Tool: PyInstaller
Automation: GitHub Actions
--Credits

Uses the official Umm al-Qura calendar algorithm provided by the hijridate library.

--Compatibility
This application is designed specifically for modern Windows operating systems.
✅ Supported OS: Windows Vista, Windows 7, Windows 8, Windows 10, Windows 11.
❌ Not Supported: Windows XP and older operating systems are not compatible with the required libraries.
