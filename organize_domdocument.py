import universal_functions as uf
import os
from colorama import Fore, init
init()

should_give_safe_error = False
null = None

def organize(DOMDocument, xfl_path):

    # Make list of layers that have keyframes in them
    
    layer_list = DOMDocument["timelines"]["DOMTimeline"]["layers"]["DOMLayer"]
    layer_list = uf.fix_layer_or_frame_list(layer_list)
    new_layer_list = [] # This will go in the main.xml file
    DOM_layer_list = [] # This will be kept in the DOMDocument
    for layer in layer_list:
        if layer.get("@name", "") == "instance": # If intended instance layer is already in the DOMDocument, keep it there
            DOM_layer_list.append(layer)
            continue

        frame_list = layer["frames"]["DOMFrame"]

        frame_list = uf.fix_layer_or_frame_list(uf.fix_layer_or_frame_list(frame_list), to_layer=True)

        # Check each key frame to ensure there are no sprites
        found_sprites = False
        for frame in frame_list:

            # If a frame with sprites attached is found, add to what will be main.xml
            if frame.get("elements", None) != None:
                new_layer_list.append(layer)
                found_sprites = True
                break
        # If there are none found, keep for DOMDocument
        if not found_sprites:
            DOM_layer_list.append(layer)

    # Create a new symbol file
    new_layer_list = uf.fix_layer_or_frame_list(new_layer_list)
    main_symbol = {
    "DOMSymbolItem": {
        "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "@xmlns": "http://ns.adobe.com/xfl/2008/",
        "@name": "main_sprite",
        "@symbolType": "graphic",
        "timeline": {
            "DOMTimeline": {
                "@name": "main_sprite",
                "layers": {
                    "DOMLayer": None
                }
            },
        },
    },
}
    main_symbol["DOMSymbolItem"]["timeline"]["DOMTimeline"]["layers"]["DOMLayer"] = new_layer_list

    # Write to symbol file
    main_symbol_path = os.path.join(xfl_path, "LIBRARY", "main_sprite.xml")
    uf.write_to_file(main_symbol, main_symbol_path, is_xml=True)

    # Fix labels layer to not include keyframes without sprites attached, and also rename label layer
    DOM_layer_list = fix_labels_layer(DOM_layer_list)

    # Add actions layer (which will just have stop actions, user will have to add the other keyframes themself)
    DOM_layer_list = add_action_layer(DOM_layer_list)

    # Add instance layer (which has main symbol)
    DOM_layer_list = add_instance_layer(DOM_layer_list)


        


    # Fix DOMDocument
    DOM_layer_list = uf.fix_layer_or_frame_list(DOM_layer_list)
    DOMDocument["timelines"]["DOMTimeline"]["layers"]["DOMLayer"] = DOM_layer_list
    toadd_main_symbol_inclusion = {
                         "@href": "main_sprite.xml",
                         "@itemIcon": "1",
                    }


    DOMDocument["symbols"]["Include"].append(toadd_main_symbol_inclusion)

    return DOMDocument

def add_action_layer(DOM_layer_list):
    for layer in DOM_layer_list:
        if layer.get("@name", False) == "action" or layer.get("@name", False) == "actions":
            DOM_layer_list.remove(layer)
            break
    if True:
        labels_layer = []
        for layer in DOM_layer_list:
            if layer.get("@name", False) == "label":
                labels_layer = layer
                break
        
        # Get a list of indexes to add stop actions to
        action_frame_indexes = []
        highest_index = -1
        for frame_label in labels_layer["frames"]["DOMFrame"]:
            if frame_label.get("@duration", False):
                toadd_index = int(frame_label["@index"]) + int(frame_label["@duration"]) - 1
                if toadd_index == highest_index:
                    toadd_index += 1
                action_frame_indexes.append(toadd_index)
                highest_index = toadd_index

        toadd_action_label = {
                            "@name": "action",
                            "@color": "#4F4FFF",
                            "frames": {
                                "DOMFrame": [
                                ]
                            }
                        }
        example_action_frame = lambda index : {
                                        "@index": str(index),
                                        "@keyMode": "9728",
                                        "Actionscript": {
                                            "script": "stop();"
                                        },
                                        "elements": null
                                    }

        toadd_action_label_frames = []
        for ind in action_frame_indexes:
            toadd_action_label_frames.append(example_action_frame(ind))
        
        total_action_label_frames = []
        highest_index = 0

        for action_frame in toadd_action_label_frames:
            current_index = int(action_frame["@index"])

            if highest_index == 0 and current_index != 0:
                total_action_label_frames.append(get_empty_frame(0, current_index))
                total_action_label_frames.append(action_frame)
                
                highest_index = current_index

            elif current_index != highest_index + 1:
                total_action_label_frames.append(get_empty_frame(highest_index, current_index-highest_index-1))
                total_action_label_frames.append(action_frame)

                highest_index = current_index

            elif current_index == highest_index + 1:
                total_action_label_frames.append(action_frame)
                highest_index = current_index

            else:
                total_action_label_frames.append(action_frame)
                
        toadd_action_label["frames"]["DOMFrame"] = total_action_label_frames
        DOM_layer_list.append(toadd_action_label)

    return DOM_layer_list

def get_empty_frame(index, duration):
    return {
                            "@index": str(index),
                            "@duration": str(duration),
                            "@keyMode": "9728",
                            "elements": null
                        }



def fix_labels_layer(DOM_layer_list):
    for layer in DOM_layer_list:
        layer_name = layer.get("@name", False)
        if layer_name in {"Labels Layer", "labels"}:
            frame_list = layer["frames"]["DOMFrame"]
            temp_frame_list = []
            previous_frame = None
            for frame in frame_list:
                if frame.get("@name", False):
                    temp_frame_list.append(frame)
                    previous_frame = frame
                    previous_frame["@duration"] = previous_frame.get("@duration", "0")
                elif "@duration" in frame and previous_frame is not None and previous_frame.get("@duration", False):
                    previous_frame["@duration"] = str(int(previous_frame["@duration"]) + int(frame["@duration"]) + 1)
            layer["frames"]["DOMFrame"] = temp_frame_list
            layer["@name"] = "label"
            layer["@color"] = "#4F4FFF"
            break
    return DOM_layer_list

def add_instance_layer(DOM_layer_list):
    for layer in DOM_layer_list:
        if layer.get("@name", False) == "instance":
            break
    else:
        labels_layer = []
        for layer in DOM_layer_list:
            if layer.get("@name", False) == "label":
                labels_layer = layer
                break
        frame_list = labels_layer["frames"]["DOMFrame"]
        duration = int(frame_list[-1]["@duration"])
        if duration == 0:
            duration = 1

        toadd_duration = duration + int(frame_list[-1]["@index"])
        
        toadd_instance_label = {
                            "@name": "instance",
                            "@color": "#4F4FFF",
                            "frames": {
                                "DOMFrame": {
                                        "@index": "0",
                                        "@duration": str(toadd_duration),
                                        "@keyMode": "9728",
                                        "elements": {
                                            "DOMSymbolInstance": {
                                                "@libraryItemName": "main_sprite",
                                                "@symbolType": "graphic",
                                                "@loop": "loop",
                                                "transformationPoint": {
                                                    "Point": null,
                                                            }
                                                        }
                                                    }
                                            }
                                        }
                                }
        DOM_layer_list.append(toadd_instance_label)

    return DOM_layer_list


