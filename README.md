# Newspaper-Zombie-XFL-Converter

This is a converter for the XFLs made by Newspaper Zombie (https://drive.google.com/drive/folders/10KsUxHu_9LJaSKAAaAeLCq2rSOmQCNHv). His assets are not game compatible, which will lead to tedious work by the user to convert them. This converter will handle the tedious work to help make the XFLs fit the PAM format that is needed.

# Note
You MUST have knowledge on how PAMs work in order to use this converter. You must also have Sen 4.0 and Adobe Animate to use this too. 

# What the converter will do
- Move all keyframes from the main document to main_sprite
- Split up layers that use multiple different symbols
- Organize the library into image, sprite, and media
- Fix the names of symbols
- Rename all sprites to be (prefix)_(number), like zombie_tutorial_1

# How to use
1. Download the converter in the releases tab to the right
2. Unzip the file and get the EXE inside
3. Download an XFL from Newspaper Zombie's drive (https://drive.google.com/drive/folders/10KsUxHu_9LJaSKAAaAeLCq2rSOmQCNHv) by clicking the three dots on a folder then pressing "download"
4. Open the zip and grab a folder that directly leads to the xfl (as in, the files anim.xfl and DOMDocument.xml is there)
5. Open the converter EXE
6. A prompt will show up, enter the prefix you want the xfl to use. This will be what all the sprites will use and what the XFL will be named as
7. Press ENTER and the prompt will then ask for the XFL folder. Drag the XFL folder to the prompt and press ENTER
8. Wait for the converter to do its work, pay attention to any messages that pop up.
9. Once it says complete, you now got a (mostly) working XFL. The prompt will let you know where the XFL will now be stored.
10. The next steps will be the most difficult. You will need to open the XFL in animate. You will notice there is a folder named "unknown". These will be any symbols and their attached bitmaps that you will need to adjust. There isn't any defined way to do this, but you will need to figure out a way to keep the symbols while fixing the PAM structure.
11. Once that is done, you may want to do some other adjustments to the PAM to fit any attached plant or zombie class, such as adding use_actions.
12. Open the XFL in Sen, use Flash to PAM. When prompted, ensure `split labels` is set to FALSE, otherwise the PAM will not pack. Once that is done, you have a fully functional PAM!
