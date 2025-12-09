📁 USB Sync Automation – README

📌 1. What This Project Does

This project automatically syncs files between your computer and a USB drive whenever the USB is inserted.

✔ Features

Detects a specific USB drive by its UUID

Syncs new and updated files in both directions:

From PC → USB

From USB → PC

Handles:

New files

Modified files

Directories and nested content

Uses shutil for file copying and modification time comparison

Runs automatically when the USB is plugged in (via udev rule)

✔ Typical Use Cases

Automatic backup system

Keeping a portable development folder in sync

Auto-copying school/work files

Mirroring a folder between PC and USB

⚙️ 2. How to Automate Sync Using udev (Linux)

Automation is done using a udev rule, which triggers your Python script whenever your USB drive is inserted.

Step 1: Find Your USB’s UUID

Plug in your USB and run:

lsblk -o NAME,UUID,VENDOR,MODEL


Example output:

sdb1   1234-ABCD  SanDisk  Cruzer_Blade


Copy your partition UUID (e.g., 1234-ABCD).

Step 2: Make Your Python Script Executable

At the top of your script (sync_script.py), add:

#!/usr/bin/env python3


Then:

chmod +x /home/tumelo/sync_script.py

Step 3: Create a udev Rule

Create a new udev rule file:

sudo nano /etc/udev/rules.d/99-usb-sync.rules


Add this (replace the UUID and script path):

ACTION=="add", \
SUBSYSTEM=="block", \
ENV{ID_FS_UUID}=="1234-ABCD", \
RUN+="/usr/bin/python3 /home/tumelo/sync_script.py"

Step 4: Reload udev Rules

Apply the new rule:

sudo udevadm control --reload-rules
sudo udevadm trigger

Step 5: Test the Automation

Unplug your USB → plug it back in.

Your sync script should run automatically.

You can view logs using:

journalctl -f

✔ Important Notes

You only need to set up the UUID and udev rule once.

If you modify your Python script, you do NOT need to change the udev rule.

If you buy a new USB or format the current one, repeat Step 1.

📝 License

This project is free to use, modify, and improve.
