import os

# This script is designed to visualize the directory structure of a specified folder
# and save this structure to a text file.
# It recursively traverses all subfolders and files,
# creating a tree-like representation with labels (folder/file).
# The resulting file is saved in the root of the analyzed folder.
# Hidden files and folders are always included.
# The output filename is fixed to "folder_structure.txt".

DEFAULT_OUTPUT_FILENAME = "folder_structure.txt"

def _write_folder_tree_recursive(
    current_folder_path,
    prefix="",
    output_file=None,
    output_filename_to_exclude=None,
    root_folder_abs_path=None
):
    """
    Recursively traverses and writes the directory structure to the output file,
    excluding the output file itself from the listing if it's in the root directory.
    Always shows hidden files.

    current_folder_path: Path to the current folder being scanned.
    prefix: String used for indentation and tree lines.
    output_file: File object to write to.
    output_filename_to_exclude: The basename of the output file to exclude from the listing.
    root_folder_abs_path: Absolute path of the initial root folder being analyzed.
    """
    try:
        # Get all items in the current directory
        listed_entries = os.listdir(current_folder_path)
        listed_entries.sort()  # Sort for consistent output
    except PermissionError:
        # If access to the directory is denied, write an error message to the file
        if output_file:
            output_file.write(f"{prefix}├── [Access Denied]\n")
        return
    except FileNotFoundError: # In case the path becomes invalid during execution
        if output_file:
            output_file.write(f"{prefix}├── [Path not found - unexpected]\n")
        return

    entries_to_process = []
    current_folder_abs_path_for_check = os.path.abspath(current_folder_path)

    for entry_name in listed_entries:
        # Hidden files are always included, so no specific skip for them here.

        # Exclude the output file itself if it's in the root analyzed directory
        if (entry_name == output_filename_to_exclude and
                current_folder_abs_path_for_check == root_folder_abs_path):
            continue
        
        entries_to_process.append(entry_name)

    # Prepare pointers for tree elements
    pointers = ["├── "] * (len(entries_to_process) - 1) + ["└── "] if entries_to_process else []

    for i, entry_name in enumerate(entries_to_process):
        # Construct full path to the current item
        current_path = os.path.join(current_folder_path, entry_name)
        pointer = pointers[i]

        if os.path.isdir(current_path):
            # If it's a directory, write it and recurse
            output_file.write(f"{prefix}{pointer}{entry_name} (folder)\n")
            # Update prefix for the next level of indentation
            extension = "│   " if pointer == "├── " else "    "
            _write_folder_tree_recursive(
                current_path,
                prefix + extension,
                output_file,
                output_filename_to_exclude,
                root_folder_abs_path
            )
        elif os.path.isfile(current_path):
            # If it's a file, just write it
            output_file.write(f"{prefix}{pointer}{entry_name} (file)\n")
        else:
            # For other item types (e.g., symbolic links)
            output_file.write(f"{prefix}{pointer}{entry_name} (other)\n")


def save_directory_structure_to_file(root_folder_path):
    """
    Main function to generate the directory structure and save it to a file
    named DEFAULT_OUTPUT_FILENAME in the root_folder_path.
    Always includes hidden files.

    root_folder_path: The root folder whose structure needs to be listed.
    """
    # Check if the provided path exists
    if not os.path.exists(root_folder_path):
        print(f"Error: Path '{root_folder_path}' does not exist.")
        return

    # Check if the path is a directory
    if not os.path.isdir(root_folder_path):
        print(f"Error: Path '{root_folder_path}' is not a directory.")
        return

    # Construct the full path for the output file
    output_filepath = os.path.join(root_folder_path, DEFAULT_OUTPUT_FILENAME)
    
    # Get absolute path of the root folder for correct exclusion of the output file
    root_folder_abs_path_for_check = os.path.abspath(root_folder_path)

    try:
        # Open the file for writing with UTF-8 encoding.
        # 'w' mode will overwrite the file if it exists.
        with open(output_filepath, 'w', encoding='utf-8') as f:
            # Write the root directory name to the file
            f.write(f"{os.path.basename(root_folder_path)} (folder)\n")

            # Start the recursive traversal and writing to file
            _write_folder_tree_recursive(
                root_folder_path,
                prefix="  ", # Initial prefix for the root folder's content
                output_file=f,
                output_filename_to_exclude=DEFAULT_OUTPUT_FILENAME,
                root_folder_abs_path=root_folder_abs_path_for_check
            )

        print(f"\nFolder structure successfully saved to: {output_filepath}")

    except IOError as e:
        # I/O error (e.g., no write permission)
        print(f"Error writing to file '{output_filepath}': {e}")
    except Exception as e:
        # Other unexpected errors
        print(f"An unexpected error occurred: {e}")


# --- Script execution starts here ---
if __name__ == "__main__":
    # Prompt user for the folder path
    target_directory = input("Enter path to the folder to analyze: ")

    print(f"\nGenerating folder structure for '{target_directory}'...")
    print(f"Output will be saved to '{DEFAULT_OUTPUT_FILENAME}' in that folder.")
    print(f"Hidden files and folders will be included.")


    save_directory_structure_to_file(target_directory)

    print("Done.")