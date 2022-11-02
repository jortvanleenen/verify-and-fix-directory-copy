# Verify (and fix) directory copy
## Introduction
This is a small Python script I made to ensure the copy of a large directory tree has gone well. It verifies that 
all files from the original/first directory exist in the copy/second directory. Note that it does not check whether 
the copy/second directory contains additional files in comparison to the original/first directory. This script can, 
therefore, not be used to check whether two directories are equal to each other! It will print any found differences to 
the console, while providing the option to automatically attempt to 
fix 
all mismatches and/or missing files.

## How it works
The script goes over the files of the original/first directory recursively, per file checking two things: whether the file also exists at the same location in the copy/second directory (if not: missing) and whether both files (if found) have the same checksum and/or metadata (if not: mismatch), depending on whether the `-s/--shallow` argument is provided to the script.

## How to use
1. Download and run the script, e.g. `./VerifyDir.py <optional arguments, see -h/--help> [first directory] [second 
   directory]`.

If `-s/--shallow` is provided, only some of the files' metadata is compared to increase speed. By default we look at the content (checksum) and size.\
If `-f/--fix` is provided, the program automatically attempts to fix missing files and checksum mismatches.\
If `-fd/--fixdifference` is provided, the program automatically attempts to only fix file differences (both 
files do exist and have the same name, but are not equal).\
If `-fm/--fixmissing` is provided, the program automatically attempts to only fix missing files.

## How to contribute
If you have found (an) issue(s), do let me know by creating an issue, or, if you are feeling particularly helpful, feel free to fix it yourself and make a merge request :).
