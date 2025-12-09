#!/usr/bin/env python3

import os
import shutil
import time


def path_to_set(path):
    return set(os.listdir((path)))


##only used for moving files not directories
def diff_content(diff_sets, from_path, to_path):
    for content in diff_sets:
        temp_file = os.path.join(from_path, content)

        if os.path.isfile(temp_file):
            shutil.copy2(temp_file, to_path)
            print(f'Copied {content} to {to_path}')
        else:
            temp_to_file = os.path.join(to_path, content)
            shutil.copytree(temp_file, temp_to_file)
            print(f'Copied {content} to {to_path}')


def common_file(commons, dev_path, usb_path):
    for content in commons:

        dev_file = os.path.join(dev_path, content)
        usb_file = os.path.join(usb_path, content)

        if os.path.isfile(dev_file) and os.path.isfile(usb_file):
            try:
                temp_dev_content = os.path.join(dev_path, content)
                temp_usb_content = os.path.join(usb_path, content)

                if os.path.getmtime(temp_dev_content) > os.path.getmtime(temp_usb_content):
                    print(f"Copying newer version of {content} from dev to USB")
                    shutil.copy2(temp_dev_content, temp_usb_content)
                else:
                    print(f"Copying newer version of {content} from USB to dev")
                    shutil.copy2(temp_usb_content, temp_dev_content)

            except Exception as e:
                print(f"Error syncing {content}: {e}")


def common_dir(common, dev_path, usb_path):
    for content in common:
        dev_dir = os.path.join(dev_path, content)
        usb_dir = os.path.join(usb_path, content)

        if os.path.isdir(dev_dir) and os.path.isdir(usb_dir):
            try:
                dev_set = path_to_set(dev_dir)
                usb_set = path_to_set(usb_dir)
                commons = dev_set & usb_set  # No need for list()
                not_in_usb = dev_set - usb_set
                not_in_dev = usb_set - dev_set

                # Copy unique items
                diff_content(not_in_usb, dev_dir, usb_dir)  # ✓ Fixed direction
                diff_content(not_in_dev, usb_dir, dev_dir)

                # Recursively handle subdirectories
                common_dir(commons, dev_dir, usb_dir)  # ✓ Added recursion

                # Handle common files in this directory
                common_file(commons, dev_dir, usb_dir)  # ✓ Fixed paths

            except Exception as e:
                print(f"Error syncing directory {content}: {e}")


##paths
dev_path = "/home/tumelo/Downloads/Sgela/"
usb_path = "/media/tumelo/TUM3L0/Sgela/"
##path to sets
dev_set = path_to_set(dev_path)
usb_set = path_to_set(usb_path)
##uncommon content
not_in_usb = dev_set - usb_set
not_in_dev = usb_set - dev_set
##common content
commons = list(dev_set & usb_set)

time.sleep(3)

print("USB detected...")
## Handle directories first (recursive)
common_dir(commons, dev_path, usb_path)

## Then handle common files (timestamp comparison)
common_file(commons, dev_path, usb_path)

## Content from dev to usb
diff_content(not_in_usb, dev_path, usb_path)

## Content from usb to dev
diff_content(not_in_dev, usb_path, dev_path)

print("\nDone, enjoy the rest of your day")