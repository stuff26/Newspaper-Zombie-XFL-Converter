import os
import universal_functions as uf
from colorama import Fore, init
import shutil
import json
init()



def organize(DOMDocument, symbol_list, bitmap_list, xfl_path):

    # Move symbols
    os.makedirs(os.path.join(xfl_path, "LIBRARY", "sprite"))
    for symbol in symbol_list:
        if symbol == "main_sprite.xml": continue

        symbol_path = os.path.join(xfl_path, "LIBRARY", symbol)
        new_symbol_path = os.path.join(xfl_path, "LIBRARY", "sprite", symbol)
        shutil.move(symbol_path, new_symbol_path)

    # Move bitmaps
    os.makedirs(os.path.join(xfl_path, "LIBRARY", "media"))
    for bitmap in bitmap_list:
        bitmap_path = os.path.join(xfl_path, "LIBRARY", bitmap)
        new_bitmap_path = os.path.join(xfl_path, "LIBRARY", "media", bitmap)
        shutil.move(bitmap_path, new_bitmap_path)

    # Add new media to DOMDocument
    toadd_bitmap_instance =  lambda href, name : {
                    "@name": name,
                    "@compressionType": "lossless",
                    "@originalCompressionType": "lossless",
                    "@quality": "50",
                    "@href": href,
                }
    toadd_media_instances = []
    for bitmap in bitmap_list:
        bitmap_name = "media/" + os.path.basename(os.path.normpath(bitmap)).replace(".png", "")
        bitmap_path = "media/" + os.path.basename(os.path.normpath(bitmap))
        toadd_media_instances.append(toadd_bitmap_instance(bitmap_path, bitmap_name))

    # Add symbols to DOMDocument
    toadd_symbol_instances = lambda href :  {
                         "@href": href,
                         "@itemIcon": "1",
                    }
    toadd_symbol_instance_list = []
    for symbol in symbol_list:
        toadd_symbol_instance_list.append(toadd_symbol_instances(f"sprite/{symbol}"))
    toadd_symbol_instance_list.append(toadd_symbol_instances("main_sprite.xml"))

    
    DOMDocument["media"]["DOMBitmapItem"] = uf.fix_layer_or_frame_list(toadd_media_instances)
    DOMDocument["symbols"]["Include"] = uf.fix_layer_or_frame_list(toadd_symbol_instance_list)
    
    toadd_folder_instance = lambda name : {
                    "@name": name,
                    "@isExpanded": "false"
                }
    DOMDocument_folders = []
    for folder_type in {"media", "sprite", "image"}:
        DOMDocument_folders.append(toadd_folder_instance(folder_type))
    
    DOMDocument["folders"] = {}
    DOMDocument["folders"]["DOMFolderItem"] = DOMDocument_folders


    return DOMDocument

