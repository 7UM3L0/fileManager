import os
import shutil


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
                dev_dir = os.path.join(dev_path, content)
                usb_dir = os.path.join(usb_path, content)
                dev_set = path_to_set(dev_dir)
                usb_set = path_to_set(usb_dir)
                commons = list(dev_set & usb_set)
                not_in_usb = dev_set - usb_set
                not_in_dev = usb_set - dev_set

                diff_content(not_in_usb, usb_dir, dev_dir)
                diff_content(not_in_dev, dev_dir, usb_dir)
                common_file(commons, dev_path, usb_path)

            except Exception as e:
                print(f"Error syncing {content}: {e}")


##paths
dev_path = ""##add device path you wish to sync 
usb_path = ""##add usb path you wish to sync 
##path to sets
dev_set = path_to_set(dev_path)
usb_set = path_to_set(usb_path)
##uncommon content
not_in_usb = dev_set - usb_set
not_in_dev = usb_set - dev_set
##common content
commons = list(dev_set & usb_set)

## Handle directories first (recursive)
common_dir(commons, dev_path, usb_path)

## Then handle common files (timestamp comparison)
common_file(commons, dev_path, usb_path)

## Content from dev to usb
diff_content(not_in_usb, dev_path, usb_path)

## Content from usb to dev
diff_content(not_in_dev, usb_path, dev_path)
