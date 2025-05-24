from colorama import Fore, init
import universal_functions as uf
import os
from shutil import copytree, rmtree
import json
import xmltodict
import tkinter as tk
init()

import check_for_improper_symbols
import organize_domdocument
import split_multi_sprite_layers
import organize_library
import fix_symbol_names
import make_xfl_datajson
import fix_media_image_symbols
import make_image_symbols
import rename_media

if not uf.is_mobile():
    root = tk.Tk()
    root.withdraw()

def main():
    print(f"{Fore.LIGHTBLUE_EX}Enter the prefix you want the {Fore.GREEN}XFL {Fore.LIGHTBLUE_EX}to use (ex. {Fore.GREEN}zombie_tutorial_flag{Fore.LIGHTBLUE_EX})")
    while True:
        xfl_prefix = uf.better_user_input().lower()
        if xfl_prefix == "":
            print(f"{Fore.LIGHTMAGENTA_EX}Enter a prefix")
            continue
        break

    # Ask for XFL path
    print(f"{Fore.LIGHTBLUE_EX}Enter the {Fore.GREEN}XFL {Fore.LIGHTBLUE_EX}you want to convert")
    while True:
        tocopy_xfl_path = uf.ask_for_directory(is_file=False, look_for_files=("DOMDocument.xml", "LIBRARY",))

        error = check_for_improper_symbols.check(tocopy_xfl_path)
        if error:
            print(f"{Fore.LIGHTMAGENTA_EX}ERROR: {error} cannot be read due to it containing elements that aren't symbols or bitmaps")
            continue

        break

    # Create XFL directory
    xfl_path = os.path.join(uf.back_a_directory(tocopy_xfl_path), xfl_prefix + ".pam.xfl")
    while True:
        if os.path.exists(xfl_path): 
            try:
                rmtree(xfl_path)
            except PermissionError:
                print(f"{Fore.LIGHTMAGENTA_EX}ERROR: can't remove {Fore.GREEN}{xfl_path}")
                input(f"{Fore.LIGHTBLUE_EX}Press ENTER to attempt to clear out the directory again")
                continue
        try:
            copytree(tocopy_xfl_path, xfl_path)
        except FileExistsError:
            print(f"{Fore.LIGHTMAGENTA_EX}ERROR: could not write to {Fore.GREEN}{xfl_path}{Fore.LIGHTMAGENTA_EX}, the folder might be being used by another program")
            input(f"{Fore.LIGHTBLUE_EX}Press ENTER to attempt to clear out the directory again")
            continue
        break
    print(f"{Fore.LIGHTBLUE_EX}Cleared out {Fore.GREEN}{xfl_path}")
    
    # Get DOMDocument path
    DOMDocument_path = os.path.join(xfl_path, "DOMDocument.xml")

    # Open DOMDocument file
    DOMDocument = uf.open_xml_file(DOMDocument_path)["DOMDocument"]

    # Get list of symbols inside of DOMDocument
    symbol_list = []
    for symbol in DOMDocument["symbols"]["Include"]:
        symbol_name = symbol.get("@href", False) # Get full symbol name
            
        if symbol_name:
            symbol_list.append(symbol_name)
        
    # Get list of bitmaps inside DOMDocument
    bitmap_list = []
    for bitmap in uf.fix_layer_or_frame_list(DOMDocument["media"]["DOMBitmapItem"], to_layer=True):
        bitmap_list.append(bitmap["@href"])


    # Organize DOMDocument and move all symbols to main
    DOMDocument = organize_domdocument.organize(DOMDocument, xfl_path)
    symbol_list.append("main_sprite.xml")
    print(f"{Fore.LIGHTBLUE_EX}Organized {Fore.GREEN}DOMDocument {Fore.LIGHTBLUE_EX}and created {Fore.GREEN}main.xml")

    # Split layers that use multiple different sprites
    split_multi_sprite_layers.split(symbol_list, xfl_path)
    print(f"{Fore.LIGHTBLUE_EX}Split layers using multiple symbols")

    # Organize library
    DOMDocument = organize_library.organize(DOMDocument, symbol_list, bitmap_list, xfl_path)
    print(f"{Fore.LIGHTBLUE_EX}Organized library")

    # Rename all media to a consistent name
    DOMDocument, old_new_media_dict = rename_media.rename(DOMDocument, xfl_prefix, bitmap_list, xfl_path)

    # Make image symbols for all media
    DOMDocument = make_image_symbols.make(DOMDocument, xfl_path)

    # Fix symbol names to reference folders
    fix_symbol_names.fix(DOMDocument, xfl_path, old_new_media_dict, symbol_list)

    # Make data.json
    make_xfl_datajson.main(xfl_path, old_new_media_dict, xfl_prefix)
    print(f"{Fore.GREEN}data.json {Fore.LIGHTBLUE_EX}written")

    # Final adjustments
    DOMDocument["timelines"]["DOMTimeline"]["@name"] = "animation"
    DOMDocument["@width"], DOMDocument["@height"] = "390", "390"
    DOMDocument["@backgroundColor"] = "#666666"

    os.rename(os.path.join(xfl_path, "LIBRARY"), os.path.join(xfl_path, "library",))

    uf.write_to_file({"DOMDocument": DOMDocument,}, DOMDocument_path, is_xml=True)
    input(f"{Fore.LIGHTBLUE_EX}\nSuccessfully written new XFL to {Fore.GREEN}{xfl_path}")

    


if __name__ == "__main__":
    main()
    """
    try:
        main()
    except Exception as e:
        print(f"{Fore.LIGHTMAGENTA_EX}ERROR: {e}")"""