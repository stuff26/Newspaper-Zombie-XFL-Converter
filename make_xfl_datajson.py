from PIL import Image, UnidentifiedImageError
import os
import json
from colorama import Fore, init
from readchar import readchar
import universal_functions as uf
init()

should_give_safe_error = False
SCALE = 0.78125 # What to multiply dimensions from media by
IMAGE_PREFIX = "IMAGE_" # Image prefix to add to front of new image IDs
def main(xfl_dir, old_new_media_dict, xfl_prefix):

    # Datajson base
    datajson = {
     "version": 6,
     "resolution": 1536,
     "position": {
          "x": 0,
          "y": 0
     },
     "image": {
     },
     "sprite": {}
    }


    # Go through each image, take dimensions, calculate, and add to data.json
    library_path = os.path.join(xfl_dir, "LIBRARY")
    for bitmap in old_new_media_dict.values():
        bitmap = "media/" + bitmap.replace(".png", "")

        try:
            image_path = os.path.join(library_path, f"{bitmap}.png")
            image = Image.open(image_path)
        # If file does not exist in media folder
        except FileNotFoundError:
            print(f"{Fore.LIGHTMAGENTA_EX}Could not find {image_path}, will not be added to data.json")
            continue
        # If file can't be read by pillow
        except UnidentifiedImageError:
            print(f"{Fore.LIGHTMAGENTA_EX}{bitmap} is not an image file, will not be added to data.json")
            continue
        
        # Calculate new image sizes
        width = int(image.width * SCALE)
        height = int(image.height * SCALE)
        
        # Make ID
        bitmap = bitmap.replace("media/", "")
        image_id = adjust_prefix(xfl_prefix.upper()) + bitmap.upper()
        
        # Create new image info
        image_info = {
            "id": image_id,
            "dimension": {
                "width": width,
                "height": height,
            },
            "additional": None,
        }
        # Add to datajson + give message
        datajson["image"][bitmap] = image_info

    # Add new stuff to data.json
    uf.write_to_file(datajson, os.path.join(xfl_dir, "data.json"), is_json=True)
    
def adjust_prefix(prefix):
    # Adjust user input to make sure it starts with IMAGE_ and ends with _
    if not prefix.startswith(IMAGE_PREFIX):
        prefix = IMAGE_PREFIX + prefix
    if not prefix.endswith("_"):
        prefix += "_"
    return prefix

if __name__ == "__main__":
    if not should_give_safe_error:
        main()
        input()
        
    else:
        try:
            main()
            input("Complete")
        except Exception as e:
            print(f"{Fore.LIGHTMAGENTA_EX}ERROR: {e}")
            input()

