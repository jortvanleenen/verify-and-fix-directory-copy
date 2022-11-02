# Verify (and fix) directory copy
## Introduction
This is a small Python script I made to ensure the copy of a large directory tree has gone well. It verifies that all files from the original/first directory exist in the copy/second directory. Note that it does not check whether the copy/second directory contains additional files in comparison to the original/first directory. It will print any found differences to the console, afterwards providing a prompt whether the user would like to attempt to fix all mismatches and/or missing files.

## How it works
The script goes over the files of the original/first directory recursively, per file checking two things: whether the file also exists at the same location in the copy/second directory (if not: missing) and whether both files (if found) have the same checksum (if not: mismatch). I decided on using the XXH3 non-cryptographic hash algorithm (of the xxHash family) as it is very fast and I do not need cryptographic properties for this use-case.

## How to use
1. Install the requirements (xxhash), e.g. `pip install -r requirements.txt`.
2. Run the script, e.g. `./main.py`. *Note: The first and second directories can be provided as arguments to the script. Providing them to the CLI later when running the script is possible as well.*

## How to contribute
If you have found (an) issue(s), do let me know by creating an issue, or, if you are feeling particularly helpful, feel free to fix it yourself and make a merge request :).
