import os
import json
from colorama import Fore, init
from readchar import readchar
import universal_functions as uf
import shutil
init()

should_give_safe_error = False
def fix(DOMDocument, xfl_path, xfl_prefix, bitmap_list):

    # Get a list of all image symbols
    image_symbol_list = []
    symbols = DOMDocument["symbols"]["Include"]
    for symbol in symbols:
        href = symbol.get("@href", "")
        if href.startswith("image/"):
            image_symbol_list.append(href)

    # Make a dictionary of each image symbol and what media they use
    image_media_dict = {}
    for symbol in image_symbol_list:
        symbol_path = os.path.join(xfl_path, "LIBRARY", symbol)
        symbol_file = uf.open_xml_file(symbol_path)

        bitmap_name = symbol_file["DOMSymbolItem"]["timeline"]["DOMTimeline"]["layers"]["DOMLayer"]["frames"]["DOMFrame"]["elements"]["DOMBitmapInstance"]["@libraryItemName"]
        image_media_dict[symbol] = bitmap_name
    
    temp_num = 1
    os.makedirs(os.path.join(xfl_path, "LIBRARY", "temp_media"))
    old_new_media_dict = {}

    for media in image_media_dict:
        media_path = os.path.join(xfl_path, "LIBRARY", "media", f"{image_media_dict[media]}.png")

        new_media_name = f"{xfl_prefix}_{temp_num}"
        temp_num += 1
        
        old_new_media_dict[image_media_dict[media]] = new_media_name
        new_media_path = os.path.join(xfl_path, "LIBRARY", "temp_media", f"{new_media_name}.png")

        shutil.move(media_path, new_media_path)
        image_media_dict[media] = new_media_name
    
    unknown_bitmap_list = []
    for bitmap in bitmap_list:
        if bitmap.replace(".png", "") not in old_new_media_dict.keys():
            unknown_bitmap_list.append(bitmap.replace(".png", ""))
            old_media_path = os.path.join(xfl_path, "LIBRARY", "media", bitmap)
            new_media_path = os.path.join(xfl_path, "LIBRARY", "unknown", bitmap)
            shutil.move(old_media_path, new_media_path)
    shutil.rmtree(os.path.join(xfl_path, "LIBRARY", "media"), ignore_errors=True)
    shutil.move(os.path.join(xfl_path, "library", "temp_media"), os.path.join(xfl_path, "LIBRARY", "media"))
    
    new_image_media_dict = {}
    old_new_image_dict = {}
    for image in image_media_dict:
        image_path = os.path.join(xfl_path, "LIBRARY", image)
        new_image_name = image_media_dict[image]
        old_new_image_dict[image] = "image/" + new_image_name + ".xml"
        new_image_path = os.path.join(xfl_path, "LIBRARY", "image", f"{new_image_name}.xml")
        os.rename(image_path, new_image_path)
        new_image_media_dict[new_image_name] = image_media_dict[image]

    # Fix image symbol names
    for image in new_image_media_dict:
        symbol_path = os.path.join(xfl_path, "LIBRARY", "image", image + ".xml")
        symbol_file = uf.open_xml_file(symbol_path)
        current_symbol_name = symbol_file["DOMSymbolItem"]["@name"]
        symbol_file["DOMSymbolItem"]["timeline"]["DOMTimeline"]["@name"] = image_media_dict[f"image/{current_symbol_name}.xml"].replace(".xml", "").replace("image/", "")
        symbol_file["DOMSymbolItem"]["@name"] = "image/" + image_media_dict[f"image/{current_symbol_name}.xml"]

        uf.write_to_file(symbol_file, symbol_path, is_xml=True)
        # A later function will fix the media name inside

    # Fix DOMDocument
    #print(json.dumps(old_new_media_dict, indent=4))
    for media_instance in DOMDocument["media"]["DOMBitmapItem"]:
        key = os.path.basename(os.path.normpath(media_instance["@name"]))
        try:
            if key not in unknown_bitmap_list:
                media_instance["@name"] = "media/" + old_new_media_dict[key]
                media_instance["@href"] = "media/" + old_new_media_dict[key] + ".png"
            else:
                media_instance["@name"] = "unknown/" + key
                media_instance["@href"] = "unknown/" + key + ".png"
        except KeyError:
            continue

    for symbol_instance in DOMDocument["symbols"]["Include"]:
        href = symbol_instance["@href"]
        if href.startswith("image/"):
            symbol_instance["@href"] = old_new_image_dict[href]

    # Fix unknown image symbols
    unknown_symbols = []
    for symbol in DOMDocument["symbols"]["Include"]:
        href = symbol.get("@href", "")
        if href.startswith("unknown/"):
            unknown_symbols.append(href)

    for symbol in unknown_symbols:
        symbol_path = os.path.join(xfl_path, "LIBRARY", symbol)
        symbol_file = uf.open_xml_file(symbol_path)
        layer_list = uf.fix_layer_or_frame_list(symbol_file["DOMSymbolItem"]["timeline"]["DOMTimeline"]["layers"]["DOMLayer"], to_layer=True)
        for layer in layer_list:
            frame_list = uf.fix_layer_or_frame_list(layer["frames"]["DOMFrame"], to_layer=True)
            for frame in frame_list:
                library_item = frame["elements"]["DOMBitmapInstance"]["@libraryItemName"].replace("media/", "")
                if library_item in old_new_media_dict:
                    frame["elements"]["DOMBitmapInstance"]["@libraryItemName"] = old_new_media_dict[library_item]
                elif library_item in unknown_bitmap_list:
                    frame["elements"]["DOMBitmapInstance"]["@libraryItemName"] = "unknown/" + library_item
                else:
                    print(library_item)
            layer["frames"]["DOMFrame"] = uf.fix_layer_or_frame_list(frame_list)
        symbol_file["DOMSymbolItem"]["timeline"]["DOMTimeline"]["layers"]["DOMLayer"] =  uf.fix_layer_or_frame_list(layer_list)
        uf.write_to_file(symbol_file, symbol_path, is_xml=True)



    return (DOMDocument, old_new_image_dict, old_new_media_dict, unknown_bitmap_list)