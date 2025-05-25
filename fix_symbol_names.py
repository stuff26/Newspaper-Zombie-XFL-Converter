import os
import universal_functions as uf
from colorama import Fore, init
import json
init()


def fix(DOMDocument, xfl_path, old_new_media_dict, symbol_list, image_to_converted_symbol_dict):

    for symbol in symbol_list:
        if symbol != "main_sprite.xml":
            symbol_path = os.path.join(xfl_path, "LIBRARY", "sprite", symbol)
        else:
            symbol_path = os.path.join(xfl_path, "LIBRARY", symbol)
        symbol_file = uf.open_xml_file(symbol_path)

        # Fix main symbol name
        current_name = symbol_file["DOMSymbolItem"]["@name"]
        if symbol != "main_sprite.xml" and not symbol.startswith("image/"):
            symbol_file["DOMSymbolItem"]["@name"] = "sprite/" + current_name
        
        # Fix symbol type
        symbol_file["DOMSymbolItem"]["@symbolType"] = "graphic"

        # Fix every single frame
        layer_list = uf.fix_layer_or_frame_list(symbol_file["DOMSymbolItem"]["timeline"]["DOMTimeline"]["layers"]["DOMLayer"], to_layer=True)
        for layer in layer_list:

            frame_list = uf.fix_layer_or_frame_list(layer["frames"]["DOMFrame"], to_layer=True)
            for frame in frame_list:
                elements = frame["elements"]
                if elements == None: continue

                for element_instance in elements.copy():
                    library_item = elements[element_instance]["@libraryItemName"]
                    if element_instance == "DOMBitmapInstance":
                        elements["DOMSymbolInstance"] = elements["DOMBitmapInstance"]
                        elements["DOMSymbolInstance"]["@libraryItemName"] = "sprite/" + image_to_converted_symbol_dict["image/" + old_new_media_dict[library_item.replace(".png", "")]]
                        elements.pop("DOMBitmapInstance")
                    elif element_instance == "DOMSymbolInstance":
                        elements[element_instance]["@libraryItemName"] = "sprite/" + library_item

                frame["elements"] = elements
            layer["frames"]["DOMFrame"] = frame_list
        symbol_file["DOMSymbolItem"]["timeline"]["DOMTimeline"]["layers"]["DOMLayer"] = layer_list

        uf.write_to_file(symbol_file, symbol_path, is_xml=True)
    

