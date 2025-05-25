import universal_functions as uf
import os
from colorama import Fore, init
init()



def make(DOMDocument, xfl_path, symbol_list):

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
                                                "@ty": "0",
                                                "@a": "0.78125",
                                                "@d": "0.78125"
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
    image_symbol_list = []
    os.makedirs(os.path.join(xfl_path, "LIBRARY", "image"))
    for bitmap in bitmap_list:
        symbol_path = os.path.join(xfl_path, "LIBRARY", "image", bitmap+".xml")
        symbol_file = default_image_symbol(bitmap)
        image_symbol_list.append(f"image/{bitmap}")
        uf.write_to_file(symbol_file, symbol_path, is_xml=True)

        DOMDocument["symbols"]["Include"].append(default_symbol_instance(bitmap))


    default_sprite_adjuster = lambda image, num : {
    "DOMSymbolItem": {
        "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "@xmlns": "http://ns.adobe.com/xfl/2008/",
        "@name": f"sprite/nz_adjuster_{num}",
        "@symbolType": "graphic",
        "timeline": {
            "DOMTimeline": {
                "@name": f"nz_adjuster_{num}",
                "layers": {
                    "DOMLayer": {
                        "@name": "Layer 1",
                        "@color": "#33C2FF",
                        "frames": {
                            "DOMFrame": {
                                "@index": "0",
                                "@keyMode": "9728",
                                "elements": {
                                    "DOMSymbolInstance": {
                                        "@libraryItemName": image,
                                        "matrix": {
                                            "Matrix": {
                                                "@tx": "0",
                                                "@ty": "0",
                                                "@a": "1.27999877929688",
                                                "@d": "1.27999877929688"
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
    default_symbol_instance = lambda num :   {
                    "@href": f"sprite/nz_adjuster_{num}.xml",
                    "@itemIcon": "1",
                }
    num = 0
    image_to_converted_symbol_dict = {}
    for image in image_symbol_list:
        num += 1

        symbol_path = os.path.join(xfl_path, "LIBRARY", "sprite", f"nz_adjuster_{num}.xml")
        symbol_file = default_sprite_adjuster(image, num)
        uf.write_to_file(symbol_file, symbol_path, is_xml=True)
        image_to_converted_symbol_dict[image] = f"nz_adjuster_{num}"

        DOMDocument["symbols"]["Include"].append(default_symbol_instance(num))




    return DOMDocument, image_to_converted_symbol_dict
