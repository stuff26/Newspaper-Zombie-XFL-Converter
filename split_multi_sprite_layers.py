import universal_functions as uf
import os
from copy import deepcopy



should_give_safe_error = False
CHECKING_SYMBOL_TYPES = {"main_sprite.xml", "label/", "sprite/"}


def split(symbol_list, xfl_path):

    for symbol in symbol_list:
        symbol_path = os.path.join(xfl_path, "LIBRARY", symbol)
        symbol_file = uf.open_xml_file(symbol_path)
        layer_list = symbol_file["DOMSymbolItem"]["timeline"]["DOMTimeline"]["layers"]["DOMLayer"]

        # If layer_list is a dictionary cause of only one layer, convert to layer to make it readable by separate_layer
        layer_list = uf.fix_layer_or_frame_list(layer_list, to_layer=True)

        new_layer_list = []
        for layer in layer_list:
            new_layers = separate_layer(layer)[::-1]
            new_layer_list.extend(new_layers)

        # Convert new_layer_list back to dictionary if there still is only one layer
        if len(new_layer_list) == 1:
            new_layer_list = new_layer_list[0]

        # Otherwise, check and remove any layers with only empty frames
        else:
            temp_layer_list = []
            for layer in new_layer_list:
                if check_if_only_empty(layer):  # Keep only non-empty layers
                    temp_layer_list.append(layer)

            new_layer_list = temp_layer_list
                    

        
        symbol_file["DOMSymbolItem"]["timeline"]["DOMTimeline"]["layers"]["DOMLayer"] = new_layer_list
        uf.write_to_file(symbol_file, symbol_path, is_xml=True)

    
def separate_layer(layer):
    layer_list = []
    frame_list = layer["frames"]["DOMFrame"]
    frame_list = uf.fix_layer_or_frame_list(frame_list, to_layer=True)

    layer_name, layer_color = layer.get("@name", ""), layer.get("@color", "#FF800A")
    current_symbol = ""
    temp_num = -1

    for frame in frame_list:
        # If frames are empty, skip
        if frame["elements"] == None:
            temp_num += 1
            layer_list.insert(temp_num, [])
            layer_list[temp_num].append(frame)
            current_symbol = ""
            continue
        
        # Get symbol found in frame
        try:
            if isinstance(frame["elements"]["DOMSymbolInstance"], dict): symbol_in_frame = frame["elements"]["DOMSymbolInstance"].get("@libraryItemName")
            else: symbol_in_frame = frame["elements"]["DOMSymbolInstance"][0].get("@libraryItemName")
        except KeyError:
            symbol_in_frame = frame["elements"]["DOMBitmapInstance"].get("@libraryItemName")

        # If a different symbol is found from what is being checked, originally, or if this is the first keyframe found
        if current_symbol != symbol_in_frame:
            current_symbol = symbol_in_frame
            temp_num += 1

            # Add to list of layers as a new list
            layer_list.insert(temp_num, [])
            layer_list[temp_num].append(frame)

        # If consistent with what is found before
        else:
            layer_list[temp_num].append(frame)
    if frame_list[-1] == []:
        frame_list.pop(-1)
    
    empty_frame_dict = {
                        "@index": "0",
                        "@duration": 0,
                        "@keyMode": "9728",
                        "elements": None
                    }

    temp_num = 0
    for new_layer in layer_list:
        # If frames don't start at 0, add empty frames
        first_frame_num = int(new_layer[0]["@index"])
        if first_frame_num != 0:
            toadd_empty_frames = deepcopy(empty_frame_dict)
            toadd_empty_frames["@duration"] = first_frame_num
            new_layer.insert(0, toadd_empty_frames)
        
        # Create proper layer
        if len(new_layer) == 1: 
            new_layer = new_layer[0]
        toadd_new_layer = {
            "@name": layer_name,
            "@color": layer_color,
            "frames": {
                "DOMFrame": deepcopy(new_layer),
            },
        }
        layer_list[temp_num] = toadd_new_layer
        temp_num += 1

    # Return
    return layer_list


def check_if_only_empty(layer):
    frame_list = layer["frames"]["DOMFrame"]
    frame_list = uf.fix_layer_or_frame_list(frame_list, to_layer=True)

    for frame in frame_list:
        elements = frame.get("elements", None)
        if elements != None:
            return True
        
    return False