import os
import shutil

def copy_files_recursive(source, destination):
    if not os.path.exists(destination):
        os.mkdir(destination)

    for content in os.listdir(source):
        source_path = os.path.join(source, content)
        destination_path = os.path.join(destination, content)
        print(f"Copying {source_path} to {destination_path}")

        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
        elif os.path.isdir(source_path):
            copy_files_recursive(source_path, destination_path)