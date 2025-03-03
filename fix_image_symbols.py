import universal_functions as uf
import os
from colorama import Fore, init
from copy import deepcopy
import json
init()


should_give_safe_error = False
null = None

example_image_symbol = lambda symbol_path, symbol_name, bitmap_name, matrix : {
    "DOMSymbolItem": {
        "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "@xmlns": "http://ns.adobe.com/xfl/2008/",
        "@name": symbol_path,
        "@symbolType": "graphic",
        "@lastModified": "1740310721",
        "timeline": {
            "DOMTimeline": {
                "@name": symbol_name,
                "layers": {
                    "DOMLayer": {
                        "@name": "",
                        "@color": "#F4FFFF",
                        "frames": {
                            "DOMFrame": {
                                "@index": "0",
                                "@keyMode": "9728",
                                "elements": {
                                    "DOMBitmapInstance": {
                                        "@selected": "true",
                                        "@libraryItemName": bitmap_name,
                                        "matrix": {
                                            "Matrix": matrix,
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

def main():
    # Get XFL directory
    print(f"{Fore.LIGHTBLUE_EX}Enter the {Fore.GREEN}XFL {Fore.LIGHTBLUE_EX}you want to check through")
    #xfl_path = uf.ask_for_directory(is_file=False, look_for_files=FILES_TO_LOOK_FOR)
    xfl_path = r"C:\Users\zacha\Documents\Coding Stuff\DA Fire Wizard Zombie"

    # Get DOMDocument dir and file
    DOMDocument_dir = os.path.join(xfl_path, "DOMDocument.xml")
    DOMDocument = uf.open_xml_file(DOMDocument_dir)

    # Get list of symbols
    symbol_dicts = DOMDocument["DOMDocument"]["symbols"]["Include"]
    symbol_list = []
    for symbol in symbol_dicts:
        symbol_list.append(symbol["@href"])

    # Open each symbol
    for symbol in symbol_list:
        # Get symbol file
        symbol_path = os.path.join(xfl_path, "LIBRARY", symbol)
        symbol_file = uf.open_xml_file(symbol_path)
        symbol = symbol.replace(".xml", "")

        # Get layers
        try:
            layers = symbol_file["DOMSymbolItem"]["timeline"]["DOMTimeline"]["layers"]["DOMLayer"]
        except KeyError:
            continue

        # Check if it is a proper image symbol
        if isinstance(layers, list):
            continue
        if isinstance(layers["frames"]["DOMFrame"], list):
            continue
        elements = layers["frames"]["DOMFrame"]["elements"]
        if "DOMShape" not in elements:
            continue

        symbol_name = os.path.basename(os.path.normpath(symbol))
        bitmap = elements["DOMShape"]["fills"]["FillStyle"]["BitmapFill"]["@bitmapPath"]
        matrix = elements["DOMShape"]["fills"]["FillStyle"]["BitmapFill"]["matrix"]["Matrix"]
        matrix.pop("@a")
        matrix.pop("@d")

        toadd_image_symbol = example_image_symbol(symbol, symbol_name, bitmap, matrix)

        uf.write_to_file(toadd_image_symbol, symbol_path, is_xml=True)








if __name__ == "__main__":
    if not should_give_safe_error:
        main()
        input(f"{Fore.LIGHTMAGENTA_EX}Complete")
        
    else:
        try:
            main()
            input("Complete")
        except Exception as e:
            print(f"{Fore.LIGHTMAGENTA_EX}ERROR: {e}")
            input()