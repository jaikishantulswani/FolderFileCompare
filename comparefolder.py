import os
import hashlib
import argparse

def calculate_md5(file_path, block_size=8192):
    """Calculate MD5 hash of a file."""
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            md5.update(block)
    return md5.hexdigest()

def find_similar_files(folder1, folder2, show_not_matched=False):
    """Find similar files based on MD5 hash."""
    md5_mapping = {}
    similar_files = []

    # Calculate MD5 hash for files in folder1
    for root, dirs, files in os.walk(folder1):
        for file in files:
            file_path = os.path.join(root, file)
            md5 = calculate_md5(file_path)
            md5_mapping.setdefault(md5, []).append(file_path)

    # Check for matching files in folder2
    for root, dirs, files in os.walk(folder2):
        for file in files:
            file_path = os.path.join(root, file)
            md5 = calculate_md5(file_path)
            if md5 in md5_mapping:
                similar_files.extend(md5_mapping[md5])

    if not show_not_matched:
        return similar_files

    # Filter out files with the same MD5 hash
    all_files = set()
    for files_list in md5_mapping.values():
        all_files.update(files_list)

    not_matched_files = set(all_files) - set(similar_files)
    return not_matched_files

def main():
    parser = argparse.ArgumentParser(description="Find similar files in two folders based on MD5 hash.")
    parser.add_argument("-f1", "--folder1", required=True, help="Path to the first folder")
    parser.add_argument("-f2", "--folder2", required=True, help="Path to the second folder")
    parser.add_argument("-nt", "--show_not_matched", action="store_true", help="Show files that are similar but not matched with MD5 hash")

    args = parser.parse_args()

    folder1 = args.folder1
    folder2 = args.folder2
    show_not_matched = args.show_not_matched

    if not (os.path.exists(folder1) and os.path.exists(folder2)):
        print("Error: Both folders must exist.")
        return

    similar_files = find_similar_files(folder1, folder2, show_not_matched)

    if similar_files:
        print("Similar files found:")
        for file in similar_files:
            print(file)
    else:
        print("No similar files found.")

if __name__ == "__main__":
    main()

