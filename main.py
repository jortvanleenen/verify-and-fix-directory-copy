"""
This script can be used to verify the second/copy directory contains an
exact copy of the first/original directory's files and its layout.
This is done recursively.

It will print the files that are not equal or missing to the console.

Note that it does not check if the second directory contains more files than
the first directory.

@file
@author Jort van Leenen
@copyright GNU General Public License v3.0
"""
import shutil
import sys
import os
import xxhash
from typing import BinaryIO


def main() -> None:
    """Entry point of the script."""
    if len(sys.argv) < 3:
        print("This program recursively checks if a copy from an original "
              "directory to a copy directory has gone well.")
        print("Please enter the first/original directory:")
        first_directory = get_valid_directory()
        print("Please enter the second/copy directory:")
        second_directory = get_valid_directory()
    else:
        # Prefix/suffix removal convenience for Windows 'Copy to path' users.
        first_directory = sys.argv[1].removeprefix("'").removesuffix("'")
        second_directory = sys.argv[2].removeprefix("'").removesuffix("'")

    if not os.path.isdir(first_directory) \
            or not os.path.isdir(second_directory):
        print("An invalid directory has been entered.")
        sys.exit(1)

    if first_directory == second_directory:
        print("The directory paths are the same, no need to check.")
        return

    check_hashes(first_directory, second_directory)


def get_valid_directory() -> str:
    """Get a valid directory from the user through the CLI.

    @return the directory as a string
    """
    while True:
        path = input().removeprefix('"').removesuffix('"')
        if os.path.isdir(path):
            return path
        else:
            print("Not a valid directory, please try again.")


def get_file_hash(file: BinaryIO) -> str:
    """Get the XXH32 hash of a file.

    @param file the file to hash
    @return the hash as a string
    """
    file_hash = xxhash.xxh3_64()
    for byte_block in iter(lambda: file.read(4096), b""):
        file_hash.update(byte_block)
    return file_hash.hexdigest()


def repair_error(error_dict: dict) -> None:
    """Attempt to fix the file errors in the error list.

    @param error_dict the dictionary containing file errors, src: dest
    """
    for src, dst in error_dict.items():
        try:
            shutil.copy(src, dst)
            print(f"FIXED: '{src}' to '{dst}'")
        except OSError as e:
            print(f"ERROR: '{src}' to '{dst}' failed: {e.strerror}")


def check_hashes_result(found_error, mismatches, missing_files) -> None:
    """Print the result of the check_hashes function and, if found, ask the user
     if they want to attempt to fix the errors.

    @param found_error whether an error was found
    @param mismatches the dictionary containing the checksum mismatches
    @param missing_files the dictionary containing the missing files
    """
    if not found_error:
        print("No mismatches found.")
    else:
        print("Done!")
        if len(mismatches) > 0 and \
                input("Attempt to fix mismatches? (y/n)").lower() == 'y':
            repair_error(mismatches)
        if len(missing_files) > 0 and \
                input("Attempt to fix missing files? (y/n)").lower() == 'y':
            repair_error(missing_files)


def check_hashes(first_directory: str, second_directory: str) -> None:
    """Check if the files in the first directory are the same as the files
    in the second directory.

    It will print all the files that are not equal or missing to the console.

    @param first_directory the first/original directory
    @param second_directory the second/copy directory
    """
    found_error = False
    checksum_mismatches = {}
    missing_files = {}
    print("Starting comparison... (This may take a while)")
    for root, dirs, files in os.walk(first_directory):
        for file in files:
            first_path = os.path.join(root, file)
            second_path = first_path.replace(first_directory, second_directory)
            if os.path.isfile(second_path):
                with open(first_path, "rb") as first_file, \
                        open(second_path, "rb") as second_file:
                    first_hash = get_file_hash(first_file)
                    second_hash = get_file_hash(second_file)
                    if first_hash != second_hash:
                        print(f"NOT EQUAL: '{first_path}, '{second_path}'")
                        found_error = True
                        checksum_mismatches[first_path] \
                            = second_path.replace(file, '')
            else:
                print(f"NOT EXIST: '{first_path}' in "
                      f"'{second_path.replace(file, '')}'")
                found_error = True
                missing_files[first_path] = second_path.replace(file, '')
    check_hashes_result(found_error, checksum_mismatches, missing_files)


if __name__ == "__main__":
    main()
