# Verify and fix directory copy
## Introduction
This is a small Python-script I made to ensure the copy of a large directory tree has gone well. It verifies whether all files from the original/first directory exist in the copy/second directory. Note that it does not check whether the copy/second directory contains additional files in comparison to the original/first directory. It will print any found differences to the console, while then providing a prompt to attempt to fix some or all mismatches and/or missing files.

## How it works
The script goes over the two directories recursively, checking two things: whether both files exist (if not: missing) and whether both files have the same checksum (if not: mismatch). I decided on using the XXH3 non-cryptographic hash algorithm (of the xxHash family) as it is very fast and I do not need cryptographic properties for this use-case.

## How to use
1. pip install -r requirements.txt
2. Run the script, e.g. ./main.py. Arguments for the first and second directory can be provided as arguments. Providing them to the CLI later when running the script is possible as well.
