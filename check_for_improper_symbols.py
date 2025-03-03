import universal_functions as uf
import os


should_give_safe_error = False
acceptable_element_types = {"DOMBitmapInstance", "DOMSymbolInstance"}

def check(xfl_path):

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

    for symbol in symbol_list:
        
        symbol_path = os.path.join(xfl_path, "LIBRARY", symbol)
        symbol_file = uf.open_xml_file(symbol_path)


        layer_list = symbol_file["DOMSymbolItem"]["timeline"]["DOMTimeline"]["layers"]["DOMLayer"]
        layer_list = uf.fix_layer_or_frame_list(layer_list, to_layer=True)

        for layer in layer_list:

            frame_list = layer["frames"]["DOMFrame"]
            frame_list = uf.fix_layer_or_frame_list(frame_list, to_layer=True)

            for frame in frame_list:
                elements = frame.get("elements", "")

                if elements == None:
                    continue

                for element_type in elements:
                    if element_type not in acceptable_element_types:
                        return symbol
    return False

                
