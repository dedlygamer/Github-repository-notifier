import sys
import os

# Check if the app is running on a Mac or Windows
if sys.platform == "darwin":
    # --- MAC CODE ---
    import rumps
    
    @rumps.clicked("Check Releases")
    def check_releases(sender):
        pass # Your existing release checking function code goes here

    app = rumps.App("GitHub Release Watcher", icon="menubarTemplate.png")
    app.run()

else:
    # --- WINDOWS CODE ---
    import pystray
    from PIL import Image

    def on_clicked(icon, item):
        if str(item) == "Exit":
            icon.stop()
        elif str(item) == "Check Releases":
            pass # Call your cross-platform release checking function here

    # Load the icon image bundle
    image = Image.open("menubarTemplate.png")
    
    # Design the right-click menu for the Windows Taskbar Tray
    menu = pystray.Menu(
        pystray.MenuItem('Check Releases', on_clicked),
        pystray.MenuItem('Exit', on_clicked)
    )
    
    icon = pystray.Icon("GitHub Release Watcher", image, "Release Watcher", menu)
    icon.run()
