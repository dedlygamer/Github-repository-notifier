import os
import sys
import requests  # Assuming your release watcher uses requests to check GitHub

# 1. PATH HELPER (Fixes the "FileNotFoundError" for images inside the .exe)
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# 2. CORE LOGIC (Place your actual GitHub checking functionality inside this function)
def check_github_releases():
    print("Checking GitHub for new releases...")
    # Add your actual API calling or notification logic here
    pass

# 3. OPERATING SYSTEM CHECK
if sys.platform == "darwin":
    # --- MAC CODE ---
    import rumps

    @rumps.clicked("Check Releases")
    def mac_check(sender):
        check_github_releases()

    # Uses your template image path helper
    app = rumps.App("GitHub Release Watcher", icon=resource_path("menubarTemplate.png"))
    app.run()

else:
    # --- WINDOWS CODE ---
    import pystray
    from PIL import Image

    def windows_menu_clicked(icon, item):
        if str(item) == "Exit":
            icon.stop()
        elif str(item) == "Check Releases":
            check_github_releases()

    # Safely opens the image using the path helper inside the compiled .exe
    image = Image.open(resource_path("menubarTemplate.png"))
    
    # Creates the taskbar menu layout for Windows
    menu = pystray.Menu(
        pystray.MenuItem('Check Releases', windows_menu_clicked),
        pystray.MenuItem('Exit', windows_menu_clicked)
    )
    
    icon = pystray.Icon("GitHub Release Watcher", image, "Release Watcher", menu)
    icon.run()
