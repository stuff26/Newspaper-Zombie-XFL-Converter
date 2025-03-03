import json
import os
from readchar import readchar
from colorama import init, Fore
init()
import universal_functions as uf

should_give_safe_error = False
should_readchar = True

def main():
    
    print(f"{Fore.LIGHTBLUE_EX}Enter the {Fore.GREEN}XFL {Fore.LIGHTBLUE_EX}or individual symbol you want to check")
    xfl_dir = uf.ask_for_directory(accept_any=True, look_for_files=("DOMDocument.xml",))
    
    naming_scheme = ask_for_name_scheme()
    
    if not os.path.isfile(xfl_dir):
        symbol_list = get_symbol_list(os.path.join(xfl_dir, "DOMDocument.xml"))
    else:
        symbol_list = [xfl_dir]
    
    for symbol in symbol_list:
        if not os.path.isfile(xfl_dir):
            symbol_path = os.path.join(xfl_dir, "library", symbol)
        else:
            symbol_path = xfl_dir
        file_contents = uf.open_xml_file(symbol_path)
        
        layer_list = file_contents["DOMSymbolItem"]["timeline"]["DOMTimeline"]["layers"].get("DOMLayer", {})
        if isinstance(layer_list, dict):
            layer_list = [layer_list]
        layer_list = rename_layers(layer_list, naming_scheme)
        file_contents["DOMSymbolItem"]["timeline"]["DOMTimeline"]["layers"]["DOMLayer"] = layer_list
        uf.write_to_file(file_contents, symbol_path, is_xml=True)
        
    
    
    
    
def get_symbol_list(DOMDocument_dir):
    # Get DOMDocument
    DOMDocument = uf.open_xml_file(DOMDocument_dir)["DOMDocument"]
    
    # Get list of label and sprite symbols
    symbol_list = []
    for symbol in DOMDocument["symbols"]["Include"]:
        symbol_name = symbol.get("@href", False) # Get full symbol name
        symbol_list.append(symbol_name)
            
    # Return
    return symbol_list

def ask_for_name_scheme():
    print(f"{Fore.LIGHTBLUE_EX}What type of naming scheme do you want?")
    print(f"{Fore.LIGHTMAGENTA_EX}[1] {Fore.LIGHTGREEN_EX}By number from top to bottom(ex Layer 1, Layer 2, etc)")
    print(f"{Fore.LIGHTMAGENTA_EX}[2] {Fore.LIGHTGREEN_EX}By number from bottom to top (ex Layer 5, Layer 4, etc)")
    print(f"{Fore.LIGHTMAGENTA_EX}[3] {Fore.LIGHTGREEN_EX}By symbol used in each layer")
    
    while True:
        if should_readchar:
            answer = int(readchar())
        else:
            answer = int(input())
        if answer in (1, 2, 3):
            print(f"{Fore.YELLOW}{answer}")
            return answer

def rename_layers(layer_list, naming_scheme):
        
    if naming_scheme in (1, 2):
        num_to_change_by = 0
        if naming_scheme == 1:
            num = 1
            num_to_change_by = 1
        else:
            num = len(layer_list)
            num_to_change_by = -1
        for layer in layer_list:
            layer["@name"] = f"Layer {num}"
            num += num_to_change_by
                
                
    elif naming_scheme == 3:
        added_symbols = []
        for layer in layer_list:
            layer_index = layer_list.index(layer)
            layer, symbol_used = rename_with_symbol(layer, added_symbols)
            added_symbols.append(symbol_used)
            layer_list[layer_index] = layer
    
    return layer_list
    
    
def rename_with_symbol(layer, added_symbols):
    
    frame_list = layer["frames"]["DOMFrame"]
    symbol_used = elements = ""
    if isinstance(frame_list, dict):
        frame_list = [frame_list]
        
    for frame in frame_list:
        elements = frame.get("elements", False)
        if elements:
            if "DOMBitmapInstance" in frame["elements"].keys():
                symbol_used = frame["elements"]["DOMBitmapInstance"]["@libraryItemName"]
            if "DOMSymbolInstance" in frame["elements"].keys():
                symbol_used = frame["elements"]["DOMSymbolInstance"]["@libraryItemName"]
            break
    
    if symbol_used:
        
        def check_beginning(starting, symbol_used):
            if symbol_used.startswith(starting):
                return symbol_used[len(starting):]
            return symbol_used
                
        beginning_to_remove = ("image/", "media/", "sprite/")
        for to_remove in beginning_to_remove:
            symbol_used = check_beginning(to_remove, symbol_used)
            
        num_to_add = 1 + added_symbols.count(symbol_used)
        layer["@name"] = f"{symbol_used} {num_to_add}"
        
    return (layer, symbol_used)
    
if __name__ == "__main__":
    if not should_give_safe_error:
        main()
        input(f"{Fore.LIGHTMAGENTA_EX}Complete")
        
    else:
        try:
            main()
            #input("Complete")
        except Exception as e:
            print(f"{Fore.LIGHTMAGENTA_EX}ERROR: {e}")
            input()