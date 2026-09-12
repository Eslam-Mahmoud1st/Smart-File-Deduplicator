# Smart File Deduplicator

A Python CLI tool that scans any directory (and its subdirectories) to detect and manage duplicate files using MD5 content hashing.

## Why MD5 Hashing?
Unlike basic file cleaners that only check file names, this script reads the actual file content in chunks. This means it accurately detects identical files even if they have completely different names or extensions, while being memory-efficient with large files (like videos).

## Features
- Recursive directory scanning.
- Memory-friendly chunked file reading (`64KB` blocks).
- Interactive deletion prompt with safety default (No).

## How to Run

1. Run the script:
```bash
python dedupe.py

 * Enter the absolute or relative path of the folder you want to scan when prompted:
Enter directory path to scan: /path/to/your/folder

Or pass the path directly as an argument:
python dedupe.py /path/to/your/folder
