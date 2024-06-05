import hashlib
import json
import os
import sys
import datetime
import argparse
import re

def get_file_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def extract_platform_and_name(file_name):
    match = re.match(r"^(.*)-(\w+)(\.\w+)?$", file_name)
    if match:
        software_name, platform = match.groups()[:2]
        return software_name, platform
    return None, None

def generate_file_data(file_path, commit, software_name, software_version, is_protected):
    file_info = os.stat(file_path)
    
    file_name = os.path.basename(file_path)
    file_size = file_info.st_size
    file_creation_time = datetime.datetime.fromtimestamp(file_info.st_ctime).isoformat()
    file_md5 = get_file_md5(file_path)
    
    auto_software_name, platform = extract_platform_and_name(file_name)
    software_name = software_name if software_name else auto_software_name

    file_data = {
        "SoftwareName": software_name,
        "FileName": file_name,
        "FileMD5": file_md5,
        "FileSize": file_size,
        "SoftwareVersion": software_version,
        "FileCreationDate": file_creation_time,
        "Commit": commit,
        "Protected": is_protected,
        "Platform": platform
    }
    
    json_file_path = f"{file_name}.data.json"
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(file_data, json_file, ensure_ascii=False, indent=4)
    
    print(f"File information has been written to {json_file_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate a JSON file with file metadata.")
    
    parser.add_argument("-f", "--file", required=True, help="Path to the file on disk")
    parser.add_argument("-c", "--commit", required=True, help="Commit number of the file")
    parser.add_argument("-n", "--name", help="Name of the software (will be auto-completed if not provided)")
    parser.add_argument("-v", "--version", default="0.0.0", help="Version of the software (default: 0.0.0)")
    parser.add_argument("-p", "--protect", action="store_true", help="Indicate if the file should be protected (default: false)")
    
    args = parser.parse_args()
    
    if not os.path.isfile(args.file):
        print(f"Error: {args.file} is not a valid file.")
        sys.exit(1)
    
    generate_file_data(args.file, args.commit, args.name, args.version, args.protect)

if __name__ == "__main__":
    main()
