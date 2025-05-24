import universal_functions as uf
import os
from colorama import Fore, init
init()



def make(DOMDocument, xfl_path):

    bitmap_list = []
    for bitmap_instance in DOMDocument["media"]["DOMBitmapItem"]:
        bitmap_list.append(bitmap_instance["@name"].replace("media/", "").replace("unknown/", ""))

    default_image_symbol = lambda bitmap_name: {
    "DOMSymbolItem": {
        "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "@xmlns": "http://ns.adobe.com/xfl/2008/",
        "@name": f"image/{bitmap_name}",
        "@symbolType": "graphic",
        "timeline": {
            "DOMTimeline": {
                "@name": bitmap_name,
                "layers": {
                    "DOMLayer": {
                        "@name": "Layer 1",
                        "@color": "#33C2FF",
                        "frames": {
                            "DOMFrame": {
                                "@index": "0",
                                "@keyMode": "9728",
                                "elements": {
                                    "DOMBitmapInstance": {
                                        "@libraryItemName": f"media/{bitmap_name}",
                                        "matrix": {
                                            "Matrix": {
                                                "@tx": "0",
                                                "@ty": "0"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
    default_symbol_instance = lambda name :   {
                    "@href": f"image/{name}.xml",
                    "@itemIcon": "1",
                }
    os.makedirs(os.path.join(xfl_path, "LIBRARY", "image"))
    for bitmap in bitmap_list:
        symbol_path = os.path.join(xfl_path, "LIBRARY", "image", bitmap+".xml")
        symbol_file = default_image_symbol(bitmap)
        uf.write_to_file(symbol_file, symbol_path, is_xml=True)

        DOMDocument["symbols"]["Include"].append(default_symbol_instance(bitmap))


    return DOMDocument
