# Newspaper-Zombie-XFL-Converter

This is a converter for the XFLs made by Newspaper Zombie (https://drive.google.com/drive/folders/10KsUxHu_9LJaSKAAaAeLCq2rSOmQCNHv). His assets are not game compatible, which will lead to tedious work by the user to convert them. This converter will handle the tedious work to help make the XFLs fit the PAM format that is needed.

# Note
You MUST have knowledge on how PAMs work in order to use this converter. You must also have Sen 4.0 and Adobe Animate to use this too. 

# What the converter will do
- Move all keyframes from the main document to a symbol named `main_sprite`
- Split up layers that use multiple different symbols
- Organize the library into image, sprite, and media
- Fix the names of symbols
- Rename all sprites to be (prefix)_(number), like zombie_tutorial_1
- Create new image symbols for every bitmap and create new sprite symbols to adjust those image symbols

# How to use
Sometimes the XFLs downloaded for NZ's drive will need to preping, this what you may need to do first:
1. You will need to download and run [this script](https://github.com/Endlin-Boeingstein/Adobe-Animate-Plugins-for-PvZ2-XFL-Project/blob/main/%E8%87%AA%E5%8A%A8%E7%9F%A2%E9%87%8F%E8%BD%AC%E4%BD%8D%E5%9B%BEEdge2Bitmap.jsfl) which is included in the release .rar file. This will convert all vectors into bitmaps quickly.
2. After that, delete any bitmaps that are not used. You will also need to rename any bitmaps that end in .png to ensure there are no overlapping names
3. You will next have to ensure there are no keyframes with multiple symbols being used. You can use [this script](https://github.com/stuff26/PvZ2-Helper-Functions/blob/main/scripts/check_xfl_errors.py) or use my helper functions tool which comes with the xfl error checker. Use the tool to find where those keyframes are. You can ignore any errors that say there are layers with multiple symbol types as that will be fixed automatically. Separate any keyframes, however, that use multiple symbols

Once you are done with that, you can use the converter
1. Open the converter EXE
2. A prompt will show up, enter the prefix you want the xfl to use. This will be what all the sprites will use and what the XFL will be named as
3. Press ENTER and the prompt will then ask for the XFL folder. Drag the XFL folder to the prompt and press ENTER
4. Wait for the converter to do its work, pay attention to any messages that pop up.
5. Once it says complete, you now got a (mostly) working XFL. The prompt will let you know where the XFL will now be stored.
6. Open the XFL in animate and press SAVE. You don't have to do any actual changes, but saving the XFL in animate will allow Sen to convert it
7. Open the XFL in Sen, use Flash to PAM. When prompted, ensure `split labels` is set to FALSE, otherwise the PAM will not pack. Once that is done, you have a fully functional PAM!
