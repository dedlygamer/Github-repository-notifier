# GitHub Release Watcher (macOS)

A small Python menu-bar app that checks tracked public GitHub repositories hourly and sends macOS notifications when new published releases appear, including prereleases and betas.

## Requirements
- macOS Sequoia or another recent macOS release
- Python 3.10+ (Python 3.11 recommended)
- Internet connection

## Install and run

Open Terminal and run:

```bash
mkdir -p ~/Applications/GitHubReleaseWatcher
```

Copy this folder into `~/Applications/GitHubReleaseWatcher`, then:

```bash
cd ~/Applications/GitHubReleaseWatcher
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

A `GH` icon appears in the menu bar. Choose **Add repository…** and enter a URL such as `https://github.com/owner/project` or `owner/project`.

The first time a repository is added, current releases are saved as the baseline. Later new releases (including prereleases) trigger notifications. Use **Check now** to test manually. State is saved under `~/Library/Application Support/GitHub Release Watcher/state.json`.

## Launch at login (optional)

After testing the app, create a LaunchAgent. Replace `YOUR_MAC_USERNAME` in the plist path below with your short macOS account name (the part shown by `whoami` in Terminal).

1. In Terminal, run `whoami` and note the result.
2. Create the LaunchAgents folder:

```bash
mkdir -p ~/Library/LaunchAgents
```

3. Create `~/Library/LaunchAgents/com.local.github-release-watcher.plist` with this content, replacing `YOUR_MAC_USERNAME` everywhere:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.local.github-release-watcher</string>
  <key>ProgramArguments</key>
  <array>
    <string>/Users/YOUR_MAC_USERNAME/Applications/GitHubReleaseWatcher/.venv/bin/python</string>
    <string>/Users/YOUR_MAC_USERNAME/Applications/GitHubReleaseWatcher/main.py</string>
  </array>
  <key>WorkingDirectory</key><string>/Users/YOUR_MAC_USERNAME/Applications/GitHubReleaseWatcher</string>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string>/tmp/github-release-watcher.log</string>
  <key>StandardErrorPath</key><string>/tmp/github-release-watcher-error.log</string>
</dict>
</plist>
```

4. Load it:

```bash
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.local.github-release-watcher.plist
```

To stop autostart:

```bash
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.local.github-release-watcher.plist
```

Note: this Python version runs as a background menu-bar process, not a signed standalone `.app` bundle. Keep the project folder in the same location after enabling autostart. macOS notifications must be allowed for Python/Terminal if prompted. The Mac must be awake and connected to the internet for checks to run.

## Troubleshooting
- If `python3` is missing, install Python 3 from https://www.python.org/downloads/macos/.
- If `pip install` fails, ensure the Mac has internet and retry the install commands.
- If notifications do not appear, open **System Settings → Notifications** and allow notifications for the process that launched the app. Check Focus mode as well.
- Public unauthenticated GitHub API access is rate-limited. For a very large watch list, checks may occasionally fail; wait and retry.

## Notes
- Checks happen at launch and then every 60 minutes while the process is running. A sleeping/off Mac cannot check.
- GitHub's Releases API returns published releases, including prereleases; ordinary Git tags without a GitHub Release are not included.
- The API fetches the newest 100 releases per repository per check.
