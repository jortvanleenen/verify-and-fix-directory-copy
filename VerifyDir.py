"""
This script can be used to verify the second/copy directory contains an
exact copy of the first/original directory's files and its layout.
This is done recursively.

It will print the files that are not equal or missing to the console.

Note the distinction that it does not check whether two directories are equal.

@file
@author Jort van Leenen
@copyright GNU General Public License v3.0
"""
import filecmp
import shutil
import sys
import os
import argparse


def main() -> None:
    """Entry point of the script."""
    parser = argparse.ArgumentParser(
        description="This program recursively checks if a copy from an"
                    " original directory to a copy directory has gone well.",
        epilog='Made by Jort van Leenen')
    parser.add_argument('-s', '--shallow', action='store_true', default=False,
                        help='Only compare certain metadata, not content')
    parser.add_argument('-f', '--fix', action='store_true',
                        help='Fix all file errors automatically')
    parser.add_argument('-fd', '--fixdifference', action='store_true',
                        help='Only fix file difference errors automatically')
    parser.add_argument('-fm', '--fixmissing', action='store_true',
                        help='Only fix missing file errors automatically')
    parser.add_argument('first_directory', help='The original directory')
    parser.add_argument('second_directory', help='The copy directory')
    args = parser.parse_args()

    # Prefix/suffix removal convenience for Windows 'Copy to path' users.
    first_directory = args.first_directory.removeprefix("'").removesuffix("'")
    second_directory = args.second_directory.removeprefix("'").removesuffix("'")

    if not os.path.isdir(first_directory) \
            or not os.path.isdir(second_directory):
        print("An invalid directory has been entered.")
        sys.exit(1)

    if first_directory == second_directory:
        print("The directory paths are the same, no need to check.")
        return

    check_hashes(first_directory, second_directory, args)


def check_hashes(first_directory: str, second_directory: str,
                 args) -> None:
    """Check if the files in the first directory are the same as the files
    in the second directory.

    It will print all the files that are not equal or missing to the console.

    @param first_directory the first/original directory
    @param second_directory the second/copy directory
    @param args the arguments passed to the script
    """
    checksum_mismatches = {}
    missing_files = {}
    print("Starting comparison... (This may take a while)")
    for root, dirs, files in os.walk(first_directory):
        for file in files:
            first_path = os.path.join(root, file)
            second_path = first_path.replace(first_directory, second_directory)
            if os.path.isfile(second_path):
                if not filecmp.cmp(first_path, second_path, args.shallow):
                    print(f"NOT EQUAL: '{first_path}, '{second_path}'")
                    checksum_mismatches[first_path] \
                        = second_path.replace(file, '')
            else:
                print(f"NOT EXIST: '{first_path}' in "
                      f"'{second_path.replace(file, '')}'")
                missing_files[first_path] = second_path.replace(file, '')
    if len(checksum_mismatches) > 0 or len(missing_files) > 0:
        print("Done.")
        if len(missing_files) > 0 and (args.fix or args.fixmissing):
            repair_error(missing_files)
        if len(checksum_mismatches) > 0 and (args.fix or args.fixdifference):
            repair_error(checksum_mismatches)
    else:
        print("Done, no file errors found.")


def repair_error(error_dict: dict) -> None:
    """Attempt to fix the file errors in the error list.

    @param error_dict the dictionary containing file errors. src -> dst (copy)
    """
    unfixed_errors = [()]
    for src, dst in error_dict.items():
        try:
            if not os.path.isdir(dst):
                os.makedirs(dst)
            shutil.copy2(str(src), str(dst))
            print(f"FIXED: '{src}' to '{dst}'")
        except OSError as e:
            # add 3-tuple of src, dst and exception
            unfixed_errors.append((src, dst, e))
    for src, dst, e in unfixed_errors:
        print(f"ERROR: '{src}' to '{dst}' failed: {e.strerror}")


if __name__ == "__main__":
    main()
