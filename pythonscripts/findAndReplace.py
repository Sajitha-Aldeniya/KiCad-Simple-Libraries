import os

# findWord = "RG_"
# replaceWord = "SL_"
# fileExtention = ".kicad_sym"
# fileDirectory = "symbols/"



findWord = "com_github_RoboticGen_RGen-KiCAD-Libraries/RG_"
replaceWord = "com_github_Sajitha-Aldeniya_KiCad-Simple-Libraries/SL_"
fileExtention = ".kicad_mod"
fileDirectory = "footprints/"



def rename_cb_to_rg(directory):
    # Get the list of all files and directories in the current directory
    dir_contents = os.listdir(directory)

    # Loop through all files and directories in the current directory
    for item in dir_contents:
        # Construct the full path to the item
        item_path = os.path.join(directory, item)

        # Check if the item is a file
        if os.path.isfile(item_path):
            # Check if the file is a .kicad_sym file
            if item.endswith(fileExtention):
                # Read the file contents into a string
                with open(item_path, "r") as file:
                    file_contents = file.read()

                # Replace "CB_" with "RG_" in the file contents
                new_contents = file_contents.replace(findWord, replaceWord)

                # Write the updated contents back to the file
                with open(item_path, "w") as file:
                    file.write(new_contents)

        # Check if the item is a directory
        elif os.path.isdir(item_path):
            # Recursively call the function for subdirectories
            rename_cb_to_rg(item_path)

#fileDirectory = "symbols/"
rename_cb_to_rg(fileDirectory)
