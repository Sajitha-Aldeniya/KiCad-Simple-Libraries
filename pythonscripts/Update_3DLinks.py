import os

# Define the directory to search for .kicad_mod files in
dir_to_search = "pcm/footprints"

# Walk through the directory and its subdirectories
for root, dirs, files in os.walk(dir_to_search):
    # Loop through all files in the current directory
    for file_name in files:
        # Check if the file is a .kicad_mod file
        if file_name.endswith(".kicad_mod"):
            # Construct the full path to the file
            file_path = os.path.join(root, file_name)

            # Open the file in read mode
            with open(file_path, "r") as file:
                # Read the file contents into a string variable
                file_contents = file.read()

            # Replace all occurrences of "{KICAD6_3RD_PARTY}" with "{KICAD7_3RD_PARTY}"
            new_contents = file_contents.replace("{KICAD6_3RD_PARTY}", "{KICAD7_3RD_PARTY}")

            # Open the file in write mode and write the new contents to it
            with open(file_path, "w") as file:
                file.write(new_contents)
