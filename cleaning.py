import os
import xml.etree.ElementTree as ET
import re

# Define absolute paths based on your Windows setup
ANNOTATION_DIR = r"C:\Me\Queens\3rd Year\Winter\ELEC 390\DuckDash-Online-Thingy\DuckDash-Online-Thingy\annotations"

# Define specific teams for filename fixes
FIX_FILENAME_TEAMS = {"49", "28"}  # Fix filenames for teams 49 and 28

def clean_xml_files():
    for xml_file in os.listdir(ANNOTATION_DIR):
        if not xml_file.endswith(".xml"):
            continue  # Skip non-XML files

        xml_path = os.path.join(ANNOTATION_DIR, xml_file)
        tree = ET.parse(xml_path)
        root = tree.getroot()
        modified = False  # Track changes

        # Extract the group number from the filename
        filename_tag = root.find("filename")
        path_tag = root.find("path")

        if filename_tag is not None:
            current_filename = filename_tag.text
            match = re.match(r"team(\d+)_\d+", current_filename)  # Extract team number
            
            if match:
                team_number = match.group(1)

                # Step 1: Remove <polygon> elements (for ANY team that has them)
                for obj in root.findall("object"):
                    polygon = obj.find("polygon")
                    if polygon is not None:
                        obj.remove(polygon)  # Remove polygon tag
                        modified = True
                        print(f"Removed polygon from {xml_file} (Team {team_number})")

                # Step 2: Fix incorrect filenames for teams 49 and 28
                if team_number in FIX_FILENAME_TEAMS:
                    corrected_filename = re.sub(r"_jpg\.rf\..*?\.jpg", ".jpg", current_filename)
                    if corrected_filename != current_filename:
                        print(f"Fixing filename: {current_filename} → {corrected_filename}")
                        filename_tag.text = corrected_filename
                        modified = True

                        # Fix path to match new filename
                        if path_tag is not None:
                            path_tag.text = corrected_filename

        # Save modifications if changes were made
        if modified:
            tree.write(xml_path)
            print(f"✅ Updated {xml_file}")

if __name__ == "__main__":
    clean_xml_files()
    print("\n✅ XML cleanup completed: Polygons removed from all teams, filenames fixed for teams 49 & 28!")
