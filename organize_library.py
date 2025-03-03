import os
import universal_functions as uf
from colorama import Fore, init
import shutil
import json
init()



old_new_file_dict = {}
def organize(DOMDocument, symbol_list, bitmap_list, xfl_path):

    # Make new folders
    library_path = os.path.join(xfl_path, "LIBRARY")
    folders_to_make = {"sprite", "image", "media"}
    for folder in folders_to_make:
        os.makedirs(os.path.join(library_path, folder), exist_ok=True)

    # Go through each symbol, make dictionary of where each symbol belongs
    symbol_dict = {
        "image": [],
        "sprite": [],
        "unknown": [],
    }
    for symbol in symbol_list:
        if symbol == "main_sprite.xml":
            continue

        is_image = True
        is_sprite = True

        symbol_path = os.path.join(library_path, symbol)
        symbol_file = uf.open_xml_file(symbol_path)

        layer_list = symbol_file["DOMSymbolItem"]["timeline"]["DOMTimeline"]["layers"]["DOMLayer"]
        layer_list = uf.fix_layer_or_frame_list(layer_list, to_layer=True)
        if len(layer_list) != 1:
            is_image = False

        for layer in layer_list:
            
            if is_image == False and is_sprite == False:
                break

            frame_list = layer["frames"]["DOMFrame"]
            frame_list = uf.fix_layer_or_frame_list(frame_list, to_layer=True)
            if len(frame_list) != 1:
                is_image = False

            for frame in frame_list:
                if is_image == False and is_sprite == False:
                    break

                elements = frame.get("elements", None)
                if elements == None:
                    continue

                if elements.get("DOMBitmapInstance", False):
                    is_sprite = False
                if elements.get("DOMSymbolInstance", False):
                    is_image = False
                for element_type in elements:
                    if element_type not in {"DOMBitmapInstance", "DOMSymbolInstance"}:
                        is_sprite = False
                        is_image = False


        if is_image:
            symbol_dict["image"].append(symbol)
        elif is_sprite:
            symbol_dict["sprite"].append(symbol)
        else:
            print(f"{Fore.LIGHTMAGENTA_EX}Could not determine what type of symbol {Fore.GREEN}{symbol} {Fore.LIGHTMAGENTA_EX}is, will be placed in unknown folder")
            symbol_dict["unknown"].append(symbol)

    # Make unknown folder if it exists
    if symbol_dict["unknown"] != []:
        os.makedirs(os.path.join(library_path, "unknown"), exist_ok=True)

    # Remove any instance already existing folders
    DOMDocument_folders = DOMDocument.get("folders", {}).get("DOMFolderItem", False)
    if DOMDocument_folders and isinstance(DOMDocument_folders, dict):
        temp_DOMDocument_folders = []
        for folder_instance in DOMDocument_folders:
            if not("@name" in {"media", "sprite", "image", "unknown"}):
                temp_DOMDocument_folders.append(folder_instance)
        DOMDocument["folders"]["DOMFolderItem"] = temp_DOMDocument_folders


    # Move symbols and make folders
    folders_to_add = []
    for symbol_type in symbol_dict:
        folders_to_add.append({
                    "@name": symbol_type,
                    "@isExpanded": "true",
                })
        for symbol in symbol_dict[symbol_type]:
            old_new_file_dict[symbol.replace(".xml", "")] = f"{symbol_type}/{os.path.basename(os.path.normpath(symbol))}".replace(".xml", "")
            old_symbol_path = os.path.join(library_path, symbol)
            new_symbol_path = os.path.join(library_path, symbol_type, os.path.basename(os.path.normpath(symbol)))
            shutil.move(old_symbol_path, new_symbol_path)

    # Move bitmaps
    folders_to_add.append({
                    "@name": "media",
                    "@isExpanded": "true",
                })
    for bitmap in bitmap_list:
        old_new_file_dict[bitmap.replace(".png", "")] = f"media/{os.path.basename(os.path.normpath(bitmap))}".replace(".png", "")
        old_bitmap_path = os.path.join(library_path, bitmap)
        new_bitmap_path = os.path.join(library_path, "media", os.path.basename(os.path.normpath(bitmap)))
        shutil.move(old_bitmap_path, new_bitmap_path)


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
    for symbol_type in symbol_dict:
        for symbol in symbol_dict[symbol_type]:
            toadd_symbol_instance_list.append(toadd_symbol_instances(f"{symbol_type}/{symbol}"))
    toadd_symbol_instance_list.append(toadd_symbol_instances("main_sprite.xml"))

    
    DOMDocument["media"]["DOMBitmapItem"] = toadd_media_instances
    DOMDocument["symbols"]["Include"] = uf.fix_layer_or_frame_list(toadd_symbol_instance_list)
    if DOMDocument_folders:
        DOMDocument_folders.extend(folders_to_add)
    else:
        DOMDocument_folders = folders_to_add
    DOMDocument["folders"] = {}
    DOMDocument["folders"]["DOMFolderItem"] = DOMDocument_folders


    return (DOMDocument, old_new_file_dict)

