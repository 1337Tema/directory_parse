# Project Structure Exporter

This Python script generates a textual representation of a specified folder's structure. It can optionally include the content of recognized text files, making it ideal for creating a comprehensive context of a software project for Large Language Models (LLMs) or for general project documentation and understanding.

## Features

*   **Recursive Traversal:** Scans the target directory and all its subdirectories.
*   **Clear Tree-Like Output:** Displays the folder and file hierarchy in an easy-to-read tree format.
*   **Optional File Content Inclusion:** Can include the textual content of files.
*   **Selective Content Parsing:**
    *   Only attempts to parse content for files with extensions defined in the `TEXT_FILE_EXTENSIONS` list (configurable).
    *   Indicates if a file is considered non-text or has an unrecognized extension.
*   **Multi-Encoding Support:** Attempts to read text files using a list of common encodings (`UTF-8`, `CP1251`, `CP1252`, `Latin-1`, `UTF-16`) and reports which encoding was successfully used.
*   **Output File Exclusion:** Automatically excludes its own output files (`folder_structure.txt`, `folder_structure_with_content.txt`) from the generated listing if they are in the root of the analyzed directory.
*   **Hidden File Inclusion:** By default, hidden files and folders (e.g., those starting with a `.`) are included in the structure.
*   **Error Handling:** Gracefully handles `PermissionError` for inaccessible folders and `FileNotFoundError`.
*   **Dual Output Files:**
    1.  A file with only the folder structure.
    2.  An optional second file with the folder structure *and* the content of recognized text files.
*   **Configurable Max Lines:** Limits the number of lines included from each file's content (`MAX_FILE_CONTENT_LINES`).
*   **Content Skipping:** When generating the "structure with content" file, it intelligently skips trying to parse the content of the "structure only" file if it exists.

## Prerequisites

*   Python 3.x (developed and tested with Python 3.6+)
*   No external libraries are required (uses only the standard `os` module).

## How to Use

1.  **Save the Script:** Save the Python code as a `.py` file (e.g., `export_structure.py`).
2.  **Run from Terminal:** Open your terminal or command prompt.
3.  **Execute:** Run the script using Python:
    ```bash
    python export_structure.py
    ```
4.  **Follow Prompts:**
    *   The script will first ask you to: `Enter path to the folder to analyze:`
    *   Then, it will ask: `Include text file content? ... (yes/no) [no]:`
      Enter `yes` or `y` to include content, or `no` (or press Enter for default) for structure only.

## Output

The script generates one or two `.txt` files in the **root of the analyzed folder**:

1.  **`folder_structure.txt`** (Always generated):
    *   Contains only the folder and file hierarchy.
    *   Example:
        ```
        project_root (folder)
          ├── src (folder)
          │   ├── main.py (file)
          │   └── utils.py (file)
          ├── docs (folder)
          │   └── README.md (file)
          └── .gitignore (file)
        ```

2.  **`folder_structure_with_content.txt`** (Generated if you choose to include content):
    *   Contains the full hierarchy *plus* the content of recognized text files.
    *   Content is indented under each respective file entry.
    *   Indicates the encoding used to read each file's content.
    *   Shows a message if a file is considered non-text, has an unrecognized extension, or if its content cannot be decoded.
    *   File content is limited by `MAX_FILE_CONTENT_LINES`.
    *   Example snippet:
        ```
        project_root (folder)
          ├── src (folder)
          │   ├── main.py (file)
          │   │   ┆ --- File Content (text, encoding: utf-8, up to 1000000000 lines) ---
          │   │   ┆ import os
          │   │   ┆
          │   │   ┆ def hello():
          │   │   ┆     print("Hello, World!")
          │   │   ┆
          │   │   ┆ if __name__ == "__main__":
          │   │   ┆     hello()
          │   │   ┆ --- File Content End ---
          │   └── utils.py (file)
          │       ┆ --- File Content (text, encoding: utf-8, up to 1000000000 lines) ---
          │       ┆ # Utility functions
          │       ┆ def helper_function():
          │       ┆     return True
          │       ┆ --- File Content End ---
          └── README.md (file)
              ┆ --- File Content (text, encoding: utf-8, up to 1000000000 lines) ---
              ┆ # Project Title
              ┆ This is the README.
              ┆ --- File Content End ---
        ```

## Customization

You can modify the following constants at the beginning of the script to tailor its behavior:

*   **`TEXT_FILE_EXTENSIONS`**: A Python `set` of file extensions (lowercase, including the leading dot, e.g., `.py`, `.txt`) that the script should consider as text files. Add or remove extensions as needed. An empty string `''` is included to attempt parsing files with no extension.
*   **`ENCODINGS_TO_TRY_FOR_CONTENT`**: A Python `list` of character encodings (e.g., `'utf-8'`, `'cp1251'`) that the script will attempt, in order, when trying to read file content.
*   **`MAX_FILE_CONTENT_LINES`**: An integer specifying the maximum number of lines to include from each text file's content. Default is very large.
*   **`STRUCTURE_ONLY_FILENAME`**: The filename for the structure-only output.
*   **`STRUCTURE_WITH_CONTENT_FILENAME`**: The filename for the output that includes file content.

## Use Cases

*   **LLM Context Priming:**
    The primary motivation for this script is to generate a comprehensive textual snapshot of a project. This output (especially `folder_structure_with_content.txt`) can be fed directly to Large Language Models (e.g., GPT-4, Claude, Gemini) to provide them with the necessary context about a codebase, significantly improving their ability to:
    *   Answer questions about the project.
    *   Generate relevant code snippets.
    *   Assist with debugging.
    *   Help with refactoring.
    *   Summarize project components.
*   **Project Documentation:**
    *   Quickly create an overview of a project's structure for new team members.
    *   Archive a snapshot of a project's layout.
    *   Help in understanding the organization of legacy systems.
*   **Code Review Preparation:**
    *   Share a structured view of changes or specific project areas before a code review session.
*   **Personal Reference:**
    *   Quickly get a bird's-eye view of a complex directory.

## Limitations and Notes

*   **Large Files/Projects:** For very large projects or files with extensive content, the `folder_structure_with_content.txt` file can become extremely large. The `MAX_FILE_CONTENT_LINES` setting helps mitigate this for individual files, but the overall output can still be substantial.
*   **Binary File Handling:** The script identifies text files primarily by their extension. If a binary file happens to have an extension listed in `TEXT_FILE_EXTENSIONS`, the script might attempt to read it, potentially resulting in garbled output or errors. The multi-encoding trial helps, but it's not a foolproof binary detection.
*   **Encoding Detection:** While several common encodings are attempted, it's possible that some files with less common or mixed encodings might not be decoded correctly.
*   **Performance:** For extremely large directory trees (e.g., hundreds of thousands of files), the script's execution time might increase, especially when `include_file_content` is enabled.