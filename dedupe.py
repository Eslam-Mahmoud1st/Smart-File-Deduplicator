import os
import hashlib
import sys

def get_file_hash(filepath, block_size=65536):
    """
    قراءة الملف على أجزاء لتوليد الـ MD5 Hash
    عشان ما نستهلكش الـ RAM مع الملفات الكبيرة
    """
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            buf = f.read(block_size)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(block_size)
        return hasher.hexdigest()
    except (PermissionError, FileNotFoundError):
        return None

def find_duplicates(target_directory):
    """
    البحث عن الملفات المكررة بناءً على الـ Hash
    """
    hashes = {}
    duplicates = []
    total_scanned = 0

    print(f"[*] Starting scan in: {target_directory}\n")

    for root, _, files in os.walk(target_directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            total_scanned += 1

            file_hash = get_file_hash(filepath)
            if not file_hash:
                continue

            if file_hash in hashes:
                duplicates.append((filepath, hashes[file_hash]))
            else:
                hashes[file_hash] = filepath

    return duplicates, total_scanned

def main():
    if len(sys.argv) > 1:
        folder_to_scan = sys.argv[1]
    else:
        folder_to_scan = input("Enter directory path to scan: ").strip()

    if not os.path.exists(folder_to_scan):
        print("[!] Error: Path does not exist.")
        return

    duplicates, total = find_duplicates(folder_to_scan)

    print(f"--- Scan Results ---")
    print(f"Total files scanned: {total}")
    print(f"Duplicate files found: {len(duplicates)}\n")

    if not duplicates:
        print("[+] No duplicate files found!")
        return

    for dup, original in duplicates:
        size_mb = os.path.getsize(dup) / (1024 * 1024)
        print(f"[DUPLICATE] {dup} ({size_mb:.2f} MB)")
        print(f"   Original: {original}")

        choice = input("   Delete this duplicate? (y/N): ").lower().strip()
        if choice == 'y':
            try:
                os.remove(dup)
                print("   [✓] Deleted successfully.\n")
            except Exception as e:
                print(f"   [X] Failed to delete: {e}\n")
        else:
            print("   [-] Skipped.\n")

if __name__ == "__main__":
    main()