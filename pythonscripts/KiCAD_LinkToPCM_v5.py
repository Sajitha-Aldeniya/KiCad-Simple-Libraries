import os
import json
import shutil
import zipfile
import tkinter as tk
from tkinter import filedialog

print(" Code V 4.0 ")

searchWord = "SL_"
addWord = "PCM_"
#outputDitectory = "RemovedBackup/output/"
#outputDitectory = "../RemovedBackup/output/"
outputDitectory = "pcm/symbols/"
symbolDir       = "pcm/symbols"


srcFootprint     = "footprints"
srcSymbols       = "symbols"
srcModels        = "3dmodels"
srcResources     = "resources"
srcJson          = "metadata.json"


destFootprint    = "pcm/footprints"
destSymbols      = "pcm/symbols"
destModels       = "pcm/3dmodels"
destResources    = "pcm/resources"
destJson         = "pcm/metadata.json"

packageVersion = "0.1"
kiCAD_VersionToPackage = "7"




def update_metadata():
    version = version_entry.get()
    download_size = int(download_size_entry.get())
    kicad_version = kicad_version_entry.get()
    install_size = int(install_size_entry.get())
    download_url = download_url_entry.get()

    packageVersion = version
    kiCAD_VersionToPackage = kicad_version

    print("packageVersion = " + packageVersion)
    print("kiCAD_VersionToPackage = " + kiCAD_VersionToPackage)

    # Read the content of the original "metadata.json" file
    with open("metadata.json", "r") as file:
        data = json.load(file)

    # Update the desired fields in the dictionary
    data["versions"][0]["version"] = version
    data["versions"][0]["download_size"] = download_size
    data["versions"][0]["kicad_version"] = kicad_version
    data["versions"][0]["install_size"] = install_size
    data["versions"][0]["download_url"] = download_url

    # Save the updated data to a new .json file
    updated_filename = "metadata_updated.json"
    with open(updated_filename, "w") as file:
        json.dump(data, file, indent=4)

    # Copy the updated .json file to the "pcm" directory with the same name
    shutil.copy(updated_filename, "pcm/metadata.json")

    # Delete the temporary updated .json file
    os.remove(updated_filename)

    result_label.config(text="Metadata updated and file copied successfully!")



def create_zip_archive(source_dir, dest_dir, zip_filename):
    # Create a temporary directory to hold the contents of the /pcm directory
    temp_dir = os.path.join(dest_dir, "temp")
    os.makedirs(temp_dir, exist_ok=True)

    # Copy the contents of /pcm directory to the temporary directory
    for root, _, files in os.walk(source_dir):
        for file in files:
            src_file_path = os.path.join(root, file)
            dst_file_path = os.path.join(temp_dir, os.path.relpath(src_file_path, source_dir))
            os.makedirs(os.path.dirname(dst_file_path), exist_ok=True)
            shutil.copy2(src_file_path, dst_file_path)

    # Create the .zip file in the /releases directory
    zip_filepath = os.path.join(dest_dir, zip_filename + ".zip")
    with zipfile.ZipFile(zip_filepath, "w") as zipf:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arcname)

    # Remove the temporary directory
    shutil.rmtree(temp_dir)


def create_zip_button_clicked():
    zip_filename = zip_filename_entry.get()
    if zip_filename.strip():
        pcm_directory = "pcm"
        releases_directory = "releases"
        #zip_filename = "RGen_KiCAD_V7_Libraries_v0.2.zip"
        create_zip_archive(pcm_directory, releases_directory, zip_filename)
        status_label.config(text="Zip file created successfully: {}.zip".format(zip_filename))
    else:
        status_label.config(text="Please enter a valid zip file name.")


#------------------------------------    End of Funtions    ------------------------------
###########################################################################################



#..\Landuse
sWordLen = len(searchWord)


#listFile = open("pythonscripts/LibList.txt", "r")
listFile = []

for symFilse in os.listdir("symbols/"):
    if symFilse.endswith(".kicad_sym"):
        #print(symFilse)
        listFile.append(symFilse)

print(listFile)
count = 0



for x in listFile:
    #fileName = "CB_Resistors.kicad_sym"
    #fileName = x[0:-1]
    fileName = x
    if x[0] == "#":
        continue
    
    #print("Opening File - ",  fileName)
    print(" -------------  ",fileName,"  ----------- ")
    file = open("symbols/"+fileName, "r") #Opening file
    fileData = file.read()
    fileDataLength = len(fileData)
    print(fileDataLength)
        
    #searchWord = "Arduino_Pro"
    lnCount = 1
    errorFlag_1 = True
    file.seek(0,0)
    for i in range(fileDataLength):
        #print(fileData[i])
        #print("******************")
        
        if fileData[i:i+sWordLen] == searchWord:
            count = count + 1
            for j in range(i , fileDataLength):
                errorFlag_1 = False
                if fileData[j] == '"':
                    print(count, "- ",lnCount, " ",fileData[i-1:j+1])
                    break

        if fileData[i] == "\n":
            lnCount = lnCount +1
                
    file.close()
        
    if errorFlag_1:
        print("ERROE-01 - No need of changers") 
    print("Count need to change = ", count)
    print("")



###############################################################################################
#//////////////////////////////////////////////////////////////////////////////////////////////
###############################################################################################



UserInput = input("Accept changes (y -yes / n -No to Discard) = ") 

if(UserInput == 'y'):
    print("OK **************** ")
    os.mkdir(symbolDir)
    #listFile.seek(0)
    for x in listFile:
        #fileName = "CB_Resistors.kicad_sym"
        #fileName = x[0:-1]
        fileName = x
        if x[0] == "#":
            continue
        
        #print("Opening File - ",  fileName)
        print(" -------------  ",fileName,"  ----------- ")
        file = open("symbols/"+fileName, "r") #Opening file
        fileData = file.read()
        fileDataLength = len(fileData)
        #newFileData = []
        newFileData = ""
        print(fileDataLength)
            
        #searchWord = "Arduino_Pro"
        lnCount = 1
        errorFlag_1 = True
        file.seek(0,0)
        for i in range(fileDataLength):
            #print(fileData[i])
            #print("******************")
            
            if fileData[i:i+sWordLen] == searchWord:
                count = count + 1
                #newFileData.append(addWord)
                #newFileData.append(fileData[i])
                newFileData = newFileData + addWord +fileData[i]
                for j in range(i , fileDataLength):
                    errorFlag_1 = False
                    if fileData[j] == '"':
                        print(count, "- ",lnCount, " ",fileData[i-1:j+1])
                        break
            else:
                #newFileData.append(fileData[i])
                newFileData = newFileData + fileData[i]

            if fileData[i] == "\n":
                lnCount = lnCount +1
        #print(newFileData)
        fileName = outputDitectory + fileName  
        outputFile = open(fileName, "w") #Opening file
        outputFile.write(newFileData)
        outputFile.close()

        file.close()
            
        if errorFlag_1:
            print("ERROE-01 - No changers") 
        print("Count changed = ", count)
        print("")



elif(UserInput == 'n'):
    print("Discarded **************** ")
else:
    print("Discarded **************** ")
print("")







#//////////////////////////////////////////////////////////////////////////////////////////////////
#-------------------------------    Creating PCM Package    ---------------------------------------
#//////////////////////////////////////////////////////////////////////////////////////////////////

UserInput = input("Do you want to copy other files which need to create a PCM package (y / n) = ") 

if(UserInput == 'y'):

    print("")
    print("")
    print("Copying Footprint files ........................................")
    destination = shutil.copytree(srcFootprint, destFootprint) 

    print("")
    print("Copying 3D Model files ......{ this might take some time }......")
    destination = shutil.copytree(srcModels, destModels) 

    print("")
    print("Copying metadata and resources .................................")
    destination = shutil.copytree(srcResources, destResources) 

    #outputFile = open(destJson, "w") #Opening file
    #outputFile.write(newFileData)
    #outputFile.close()

    # destination = shutil.copyfile(srcJson, destJson) 



    # Read the current values from the "metadata.json" file
    with open("metadata.json", "r") as file:
        data = json.load(file)

    # Create the GUI
    root = tk.Tk()
    root.title("Metadata Updater")

    # Create input fields and labels with default values
    version_label = tk.Label(root, text="Version:")
    version_label.grid(row=0, column=0)
    version_entry = tk.Entry(root, width= 120)
    version_entry.grid(row=0, column=1)
    version_entry.insert(0, data["versions"][0]["version"])  # Set default value

    download_size_label = tk.Label(root, text="Download Size:")
    download_size_label.grid(row=1, column=0)
    download_size_entry = tk.Entry(root, width= 120)
    download_size_entry.grid(row=1, column=1)
    download_size_entry.insert(0, str(data["versions"][0]["download_size"]))  # Set default value

    kicad_version_label = tk.Label(root, text="KiCAD Version:")
    kicad_version_label.grid(row=2, column=0)
    kicad_version_entry = tk.Entry(root, width= 120)
    kicad_version_entry.grid(row=2, column=1)
    kicad_version_entry.insert(0, data["versions"][0]["kicad_version"])  # Set default value

    install_size_label = tk.Label(root, text="Install Size:")
    install_size_label.grid(row=3, column=0)
    install_size_entry = tk.Entry(root, width= 120)
    install_size_entry.grid(row=3, column=1)
    install_size_entry.insert(0, str(data["versions"][0]["install_size"]))  # Set default value

    download_url_label = tk.Label(root, text="Download URL:")
    download_url_label.grid(row=4, column=0)
    download_url_entry = tk.Entry(root, width= 120)
    download_url_entry.grid(row=4, column=1)
    download_url_entry.insert(0, data["versions"][0]["download_url"])  # Set default value

    # Create the "Update Metadata" button
    update_button = tk.Button(root, text="Update Metadata", command=update_metadata)
    update_button.grid(row=5, columnspan=2)

    # Create a label for displaying the result
    result_label = tk.Label(root, text="")
    result_label.grid(row=6, columnspan=2)

    root.mainloop()

    print("")


else:
    print("Discarded **************** ")
print("")

UserInput = input("Do you want ReLink 3D Models to different KiCAD Version (y / n) = ")
if(UserInput == 'y'):
    print("Linking  Code Still Not Availabela")
else:
    print("Discarded 3d Linking **************** ")
print("")



UserInput = input("Do you want create the .Zip package (y / n) = ")
if(UserInput == 'y'):
    # Create the GUI
    root = tk.Tk()
    root.title("Zip File Creator")

    zipFileNameFromData = "RGen_KiCAD_V" + kiCAD_VersionToPackage + "_Libraries_v" + packageVersion
    # Create input field and label for zip file name
    zip_filename_label = tk.Label(root, text= "File Name")
    zip_filename_label.grid(row=0, column=0)
    zip_filename_entry = tk.Entry(root, width= 100)
    zip_filename_entry.grid(row=0, column=1)
    zip_filename_entry.insert(0, zipFileNameFromData)  # Set default value

    # Create the "Create Zip File" button
    create_zip_button = tk.Button(root, text="Create Zip File", command=create_zip_button_clicked)
    create_zip_button.grid(row=1, columnspan=2)

    # Create a label for displaying the status
    status_label = tk.Label(root, text="")
    status_label.grid(row=2, columnspan=2)

    root.mainloop()
    
    print("Created the .zip File ")


else:
    print("Discarded Cration of Pakage **************** ")




UserInput = input("Do you want Update the READM.md File with the latest version (y / n) = ")
if(UserInput == 'y'):
    print("Code Not availabel :[ ")
else:
    print("Discarded Updating README **************** ")




UserInput = input("Enter anything to Exit the programe :) = ") 



    
    

