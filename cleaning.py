import os
import xml.etree.ElementTree as ET
import re

# Define paths
BASE_DIR = r"c:\Nathan\Queens\3rd Year\Winter\ELEC 390\DuckDash-Online-Thingy"
ANNOTATION_DIR = os.path.join(BASE_DIR, "annotations")

def fix_filenames():
    modified_files = 0  # Track the number of files modified

    for xml_file in os.listdir(ANNOTATION_DIR):
        if not xml_file.endswith(".xml"):
            continue  # Skip non-XML files

        xml_path = os.path.join(ANNOTATION_DIR, xml_file)
        tree = ET.parse(xml_path)
        root = tree.getroot()

        filename_tag = root.find("filename")
        path_tag = root.find("path")  # Some files may contain <path> as well

        if filename_tag is not None:
            current_filename = filename_tag.text.strip()

            # Fix incorrect filename format (remove "_jpg.rf.XXXXXX.jpg")
            corrected_filename = re.sub(r"_jpg\.rf\..*?\.jpg", ".jpg", current_filename)

            # Only update the XML if changes were made
            if corrected_filename != current_filename:
                print(f"Fixing filename: {current_filename} → {corrected_filename} in {xml_file}")
                filename_tag.text = corrected_filename

                # If <path> exists, update it too
                if path_tag is not None:
                    path_tag.text = corrected_filename

                tree.write(xml_path)  # Save changes
                modified_files += 1

    print(f"\n✅ Filename correction completed. {modified_files} files updated.")

if __name__ == "__main__":
    fix_filenames()
