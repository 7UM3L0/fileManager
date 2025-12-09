import os
import shutil

def path_to_set(path):
    return set(os.listdir((path)))

##only used for moving files not directories
def diff_content(diff_sets,from_path,to_path):

    for content in diff_sets:
        temp_file = os.path.join(from_path,content)

        if not os.path.isdir(temp_file):
            shutil.copy2(temp_file,to_path)
            print(f'Moved {content} to {to_path}')
        else:
            temp_to_file = os.path.join(to_path,content)
            shutil.copytree(temp_file,temp_to_file)
            print(f'Moved {content} to {to_path}')

def common_content(commons,device_path,usb_path):

    for content in commons:
        temp_device_content = os.path.join(device_path,content)
        temp_usb_content = os.path.join(usb_path,content)

        

##paths
device_path = "/home/tumelo/Downloads"
usb_path = "/home/tumelo/temp_folder/"
##path to sets
device_set = path_to_set(device_path)
usb_set = path_to_set(usb_path)
##uncommon content
not_in_usb = device_set - usb_set
not_in_device = usb_set - device_set
##common content
commons = list(device_set & usb_set)


##content from usb to device
diff_content(not_in_device,usb_path,device_path)
##content from device to usb
diff_content(not_in_usb,device_path,usb_path)