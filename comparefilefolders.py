import os
import filecmp
import argparse
from datetime import datetime

def format_last_modified(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def find_common_files(folder1_path, folder2_path):
    # Create dictionaries to store file paths and their corresponding last modified times
    folder1_files = {}
    folder2_files = {}

    # Iterate through files in folder 1 and store their last modified times
    for root, dirs, files in os.walk(folder1_path):
        for file in files:
            file_path = os.path.join(root, file)
            last_modified = os.path.getmtime(file_path)
            folder1_files[file] = last_modified

    # Iterate through files in folder 2 and store their last modified times
    for root, dirs, files in os.walk(folder2_path):
        for file in files:
            file_path = os.path.join(root, file)
            last_modified = os.path.getmtime(file_path)
            folder2_files[file] = last_modified

    # Find common files and their last modified details
    common_files = set(folder1_files.keys()) & set(folder2_files.keys())

    # Sort the common file names
    sorted_files = sorted(common_files)

    for file in sorted_files:
        folder1_last_modified = folder1_files[file]
        folder2_last_modified = folder2_files[file]

        formatted_file = f"File: {file} "
        formatted_folder1 = f"Folder 1 Last Modified: {format_last_modified(folder1_last_modified)} "
        formatted_folder2 = f"Folder 2 Last Modified: {format_last_modified(folder2_last_modified)}"
        
        print(formatted_file + formatted_folder1 + formatted_folder2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find similar files between two folders and compare their last modified details.')
    parser.add_argument('folder1', help='Path to the first folder')
    parser.add_argument('folder2', help='Path to the second folder')
    args = parser.parse_args()

    find_common_files(args.folder1, args.folder2)

