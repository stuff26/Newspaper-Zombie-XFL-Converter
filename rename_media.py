import os
import universal_functions as uf
from colorama import Fore, init
import shutil
import json
init()



def rename(DOMDocument, xfl_prefix, bitmap_list, xfl_path):

    # Create temporary folder to move files to to prevent overlapping names
    os.makedirs(os.path.join(xfl_path, "LIBRARY", "temp_media"))

    old_new_media_dict = {}
    temp_num = 0

    for bitmap in bitmap_list:
        old_media_path = os.path.join(xfl_path, "LIBRARY", "media", f"{bitmap}")

        temp_num += 1
        new_media_name = f"{xfl_prefix}_{temp_num}"
        old_new_media_dict[bitmap.replace(".png", "")] = new_media_name

        new_media_path = os.path.join(xfl_path, "LIBRARY", "temp_media", f"{new_media_name}.png")
        shutil.move(old_media_path, new_media_path)

    # Move to media
    shutil.rmtree(os.path.join(xfl_path, "LIBRARY", "media"))
    shutil.move(os.path.join(xfl_path, "LIBRARY", "temp_media"), os.path.join(xfl_path, "LIBRARY", "media"))

    # Update DOMDocument
    for bitmap_instance in DOMDocument["media"]["DOMBitmapItem"]:
        bitmap_name = bitmap_instance["@name"].replace("media/", "")
        bitmap_instance["@name"] = "media/" + old_new_media_dict[bitmap_name]
        bitmap_instance["@href"] = "media/" + old_new_media_dict[bitmap_name] + ".png"



    return (DOMDocument, old_new_media_dict)

