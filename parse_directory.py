import os

# --- Constants ---
STRUCTURE_ONLY_FILENAME = "folder_structure.txt"
STRUCTURE_WITH_CONTENT_FILENAME = "folder_structure_with_content.txt"
MAX_FILE_CONTENT_LINES = 10e10  # Max lines of content to include per file if requested

def _write_folder_tree_recursive(
    current_folder_path,
    prefix="",
    output_file=None,
    output_filename_to_exclude=None,
    root_folder_abs_path=None,
    include_file_content=False # New parameter
):
    """
    Recursively traverses and writes the directory structure to the output file.
    Optionally includes text content of files.
    Excludes the output file itself from the listing if it's in the root directory.
    Always shows hidden files.

    current_folder_path: Path to the current folder being scanned.
    prefix: String used for indentation and tree lines for items in this folder.
    output_file: File object to write to.
    output_filename_to_exclude: The basename of the current output file to exclude.
    root_folder_abs_path: Absolute path of the initial root folder being analyzed.
    include_file_content: Boolean, whether to read and include content of files.
    """
    try:
        listed_entries = os.listdir(current_folder_path)
        listed_entries.sort()
    except PermissionError:
        if output_file:
            output_file.write(f"{prefix}├── [Access Denied]\n")
        return
    except FileNotFoundError:
        if output_file:
            output_file.write(f"{prefix}├── [Path not found - unexpected]\n")
        return

    entries_to_process = []
    current_folder_abs_path_for_check = os.path.abspath(current_folder_path)

    for entry_name in listed_entries:
        # Hidden files are always included (no specific skip for them).
        if (entry_name == output_filename_to_exclude and
                current_folder_abs_path_for_check == root_folder_abs_path):
            continue
        entries_to_process.append(entry_name)

    pointers = ["├── "] * (len(entries_to_process) - 1) + ["└── "] if entries_to_process else []

    for i, entry_name in enumerate(entries_to_process):
        current_path = os.path.join(current_folder_path, entry_name)
        item_pointer = pointers[i] # e.g., "├── " or "└── "

        if os.path.isdir(current_path):
            output_file.write(f"{prefix}{item_pointer}{entry_name} (folder)\n")
            # Determine extension for the prefix of items within this subfolder
            extension_for_next_level = "│   " if item_pointer == "├── " else "    "
            _write_folder_tree_recursive(
                current_path,
                prefix + extension_for_next_level, # New prefix for items in subfolder
                output_file,
                output_filename_to_exclude,
                root_folder_abs_path,
                include_file_content
            )
        elif os.path.isfile(current_path):
            output_file.write(f"{prefix}{item_pointer}{entry_name} (file)\n")
            if include_file_content:
                # Determine the base prefix for content lines under this file
                # It should align with the tree structure's vertical lines
                if item_pointer == "├── ":
                    content_base_prefix_ext = "│   "
                else:  # "└── "
                    content_base_prefix_ext = "    "
                
                full_content_prefix = prefix + content_base_prefix_ext + "┆ " # Using '┆' for content lines

                try:
                    with open(current_path, 'r', encoding='utf-8', errors='replace') as f_content:
                        output_file.write(f"{full_content_prefix}--- File Content (up to {MAX_FILE_CONTENT_LINES} lines) ---\n")
                        lines_written = 0
                        content_found_and_printed = False
                        for line_text in f_content:
                            if lines_written >= MAX_FILE_CONTENT_LINES:
                                output_file.write(f"{full_content_prefix}[...content truncated...]\n")
                                content_found_and_printed = True
                                break
                            output_file.write(f"{full_content_prefix}{line_text.rstrip()}\n")
                            lines_written += 1
                            content_found_and_printed = True
                        
                        if not content_found_and_printed and lines_written == 0:
                             output_file.write(f"{full_content_prefix}[File is empty or content not shown due to 0 line limit]\n")
                        
                        output_file.write(f"{full_content_prefix}--- File Content End ---\n")

                except UnicodeDecodeError:
                    output_file.write(f"{full_content_prefix}[Binary file or unreadable text encoding - Content not displayed]\n")
                except IOError as e:
                    output_file.write(f"{full_content_prefix}[Error reading file: {e}]\n")
                except Exception as e:
                    output_file.write(f"{full_content_prefix}[Unexpected error reading file content: {e}]\n")
        else:
            output_file.write(f"{prefix}{item_pointer}{entry_name} (other)\n")


def _generate_and_save_single_structure_file(
    root_folder_path,
    output_filename,
    include_file_content_flag
):
    """
    Generates the directory structure (and optionally file content)
    and saves it to the specified output_filename in the root_folder_path.
    Always includes hidden files.

    root_folder_path: The root folder whose structure needs to be listed.
    output_filename: The name of the file to save the structure to.
    include_file_content_flag: Boolean, whether to include content of files.
    """
    if not os.path.exists(root_folder_path):
        print(f"Error: Path '{root_folder_path}' does not exist.")
        return False
    if not os.path.isdir(root_folder_path):
        print(f"Error: Path '{root_folder_path}' is not a directory.")
        return False

    output_filepath = os.path.join(root_folder_path, output_filename)
    root_folder_abs_path_for_check = os.path.abspath(root_folder_path)

    try:
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(f"{os.path.basename(root_folder_path)} (folder)\n")
            _write_folder_tree_recursive(
                root_folder_path,
                prefix="  ",
                output_file=f,
                output_filename_to_exclude=output_filename, # Exclude the current output file
                root_folder_abs_path=root_folder_abs_path_for_check,
                include_file_content=include_file_content_flag
            )
        print(f"Successfully saved to: {output_filepath}")
        return True
    except IOError as e:
        print(f"Error writing to file '{output_filepath}': {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while processing '{output_filename}': {e}")
        return False

# --- Script execution starts here ---
if __name__ == "__main__":
    target_directory = input("Enter path to the folder to analyze: ")

    parse_with_content_input = input(
        "Include file content? (This will create an additional file if 'yes') (yes/no) [no]: "
    ).lower()
    should_parse_with_content = parse_with_content_input in ['yes', 'y']

    print(f"\nGenerating documentation for '{target_directory}'...")

    # 1. Always generate the structure-only file
    print(f"\nAttempting to create structure-only file: '{STRUCTURE_ONLY_FILENAME}'")
    _generate_and_save_single_structure_file(
        target_directory,
        output_filename=STRUCTURE_ONLY_FILENAME,
        include_file_content_flag=False
    )

    # 2. Optionally, generate the file with structure and content
    if should_parse_with_content:
        print(f"\nAttempting to create structure-with-content file: '{STRUCTURE_WITH_CONTENT_FILENAME}'")
        _generate_and_save_single_structure_file(
            target_directory,
            output_filename=STRUCTURE_WITH_CONTENT_FILENAME,
            include_file_content_flag=True
        )

    print("\nDocumentation generation finished.")