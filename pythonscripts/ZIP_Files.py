import os
import shutil
import zipfile

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

if __name__ == "__main__":
    pcm_directory = "pcm"
    releases_directory = "releases"
    zip_filename = "RGen_KiCAD_V7_Libraries_v0.2.zip"

    create_zip_archive(pcm_directory, releases_directory, zip_filename)

