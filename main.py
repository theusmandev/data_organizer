
import os
import shutil
from pathlib import Path
from tqdm import tqdm
import sys

def organize_files_by_extension(input_folder, output_base, exclude_extensions=None):
    """
    Organize files from input_folder into subfolders in output_base based on file extensions.
    Optimized for speed with progress bar and enhanced error handling for corrupted files.
    """
    
    copied_files = 0
    skipped_files = 0
    errors = 0

   
    input_folder = Path(input_folder).resolve()
    output_base = Path(output_base).resolve()
    print(f"🚀 Starting organization: Input = {input_folder}, Output = {output_base}")

    if not input_folder.exists():
        print(f"❌ Error: Input folder '{input_folder}' does not exist!")
        return False
    if not input_folder.is_dir():
        print(f"❌ Error: '{input_folder}' is not a directory!")
        return False

    # Ensure output base folder exists
    try:
        output_base.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"❌ Error creating output folder '{output_base}': {e}")
        return False

    exclude_extensions = set(ext.lower() for ext in (exclude_extensions or []))

    # Collect all files upfront for progress bar
    all_files = []
    try:
        for file_path in input_folder.rglob("*"):
            try:
                if file_path.is_file() and not file_path.name.startswith('.'):
                    all_files.append(file_path)
            except OSError as e:
                print(f"⏭️ Skipped unreadable file '{file_path}': {e}")
                skipped_files += 1
                errors += 1
    except Exception as e:
        print(f"❌ Error during directory traversal: {e}")
        errors += 1
        return False
    
    print(f"📄 Found {len(all_files)} valid files to process")

    # Process files with progress bar
    for file_path in tqdm(all_files, desc="Organizing files", unit="file"):
        # Extract extension
        ext = file_path.suffix.lower().lstrip(".")
        if not ext:
            ext = "no_extension"

        # Skip excluded extensions
        if ext in exclude_extensions:
            print(f"⏭️ Skipped excluded extension '{ext}' for: {file_path.name}")
            skipped_files += 1
            continue

        # Create output subfolder
        output_folder = output_base / ext
        try:
            output_folder.mkdir(exist_ok=True)
        except Exception as e:
            print(f"❌ Error creating folder '{output_folder}': {e}")
            errors += 1
            continue

        # Handle duplicate filenames
        dest_path = output_folder / file_path.name
        base_name = file_path.stem
        ext_with_dot = file_path.suffix
        counter = 1
        while dest_path.exists():
            new_name = f"{base_name}_{counter}{ext_with_dot}"
            dest_path = output_folder / new_name
            counter += 1

        # Copy file
        try:
            shutil.copy2(file_path, dest_path)
            print(f"✅ Copied: {file_path.name} → {dest_path}")
            copied_files += 1
        except (OSError, shutil.Error) as e:
            print(f"❌ Error copying '{file_path.name}' to '{dest_path}': {e}")
            errors += 1
            continue

    # Summary
    print(f"\n🎉 Organization complete!")
    print(f"📈 Summary: Copied {copied_files} files, Skipped {skipped_files} files, Errors {errors}")
    print(f"📂 Output location: {output_base}")
    return copied_files > 0

def main():
    # Example usage
    input_path = r"D:\-UNB - Copy (2)" # Replace with your input folder
    output_base = r"D:\Organized1"   # Replace with your output folder
    exclude_extensions = ['ini', 'sys', 'tmp']  # Extensions to skip

    print("📝 File Organizer Script")
    success = organize_files_by_extension(input_path, output_base, exclude_extensions)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()