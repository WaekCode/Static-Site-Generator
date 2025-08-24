import shutil
import os


#delete all the contents of the destination directory (public) to ensure that the copy is clean.
#--------------------------------------------------------------------------------------------- 
destination_path = "public" # Replace with the actual path to your directory
source_path = "static"

def delete_all_the_contents_in_the_directory(destination_path):
    # Ensure the directory exists before attempting to clear its contents
    if os.path.exists(destination_path) and os.path.isdir(destination_path):
        # Iterate over the contents of the directory
        for item in os.listdir(destination_path):
            item_path = os.path.join(destination_path, item)
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path) # Remove files or symbolic links
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path) # Remove subdirectories and their contents recursively
        print(f"Contents of '{destination_path}' cleared successfully.")
    else:
        print(f"Directory '{destination_path}' does not exist or is not a directory.")


def copy_all_the_contents_in_a_directory(source_path,destination_path):
    try:
        shutil.copytree(source_path, destination_path,dirs_exist_ok=True)
        print(f"Successfully copied '{source_path}' to '{destination_path}'")
    except FileExistsError:
        print(f"Error: Destination directory '{destination_path}' already exists.")
        print("Consider using 'dirs_exist_ok=True' to allow overwriting, or delete the destination first.")
    except Exception as e:
        print(f"An error occurred: {e}")

delete_all_the_contents_in_the_directory(destination_path)
copy_all_the_contents_in_a_directory(source_path,destination_path)