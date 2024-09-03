import os
import argparse

def renameFilesBecauseItsTheRightThingToDO(root_directories):
    """
    Renames all '.jpg' files in the specified root directories to sequentially numbered files.

    Args:
        root_directories (list of str): A list of paths to the root directories where the renaming should occur.

    Returns:
        None: The function performs file renaming operations and prints the old and new filenames to the console.
    """
    counter = 1
    for root_directory in root_directories:
        for subdir, _, files in os.walk(root_directory):
            for file in sorted(files):
                if file.endswith('.jpg'):
                    new_filename = f"{counter}.jpg"
                    old_file = os.path.join(subdir, file)
                    new_file = os.path.join(subdir, new_filename)
                    os.rename(old_file, new_file)
                    print(f"Renamed: {old_file} to {new_file}")
                    counter += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rename '.jpg' files in specified directories to sequentially numbered files.")
    parser.add_argument('root_directories', nargs='+', help="A list of root directories to process.")

    args = parser.parse_args()
    renameFilesBecauseItsTheRightThingToDO(args.root_directories)