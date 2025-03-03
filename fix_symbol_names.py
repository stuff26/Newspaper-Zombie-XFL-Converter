import os
import universal_functions as uf
from colorama import Fore, init
import json
init()


def fix(DOMDocument, old_new_file_dict, xfl_path, unknown_bitmap_list):
    new_symbol_list = []
    for symbol_instance in DOMDocument["symbols"]["Include"]:
        href = symbol_instance["@href"]
        new_symbol_list.append(href)


    for symbol in new_symbol_list:
        symbol_path = os.path.join(xfl_path, "LIBRARY", symbol)
        symbol_file = uf.open_xml_file(symbol_path)

        # Fix main symbol name
        current_name = symbol_file["DOMSymbolItem"]["@name"]
        if symbol != "main_sprite.xml" and not current_name.startswith("image/"):
            symbol_file["DOMSymbolItem"]["@name"] = old_new_file_dict[current_name]
        
        # Fix symbol type
        symbol_file["DOMSymbolItem"]["@symbolType"] = "graphic"

        # Fix every single frame
        layer_list = uf.fix_layer_or_frame_list(symbol_file["DOMSymbolItem"]["timeline"]["DOMTimeline"]["layers"]["DOMLayer"], to_layer=True)
        for layer in layer_list:

            frame_list = uf.fix_layer_or_frame_list(layer["frames"]["DOMFrame"], to_layer=True)
            for frame in frame_list:
                elements = frame["elements"]
                if elements == None:
                    continue
                if isinstance(elements, dict):
                    key_list = elements.keys()
                    for element_type in key_list:
                        if isinstance(elements[element_type], dict):
                            current_library_item = elements[element_type]["@libraryItemName"]
                            if not current_library_item.startswith("unknown/"):
                                elements[element_type]["@libraryItemName"] = old_new_file_dict[current_library_item]
                        elif isinstance(elements[element_type], list):
                            for element_type2 in elements[element_type]:
                                if isinstance(element_type2, dict):
                                    current_library_item = element_type2["@libraryItemName"]
                                    if not current_library_item.startswith("unknown/"):
                                        element_type2["@libraryItemName"] = old_new_file_dict[current_library_item]

                frame["elements"] = elements
            layer["frames"]["DOMFrame"] = frame_list
        symbol_file["DOMSymbolItem"]["timeline"]["DOMTimeline"]["layers"]["DOMLayer"] = layer_list

        uf.write_to_file(symbol_file, symbol_path, is_xml=True)
    

