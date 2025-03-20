import os
import xml.etree.ElementTree as ET
import re

# Define the path to your annotations folder
ANNOTATION_DIR = r"C:\Me\Queens\3rd Year\Winter\ELEC 390\DuckDash-Online-Thingy\DuckDash-Online-Thingy\annotations"

# Define label corrections (incorrect XML name → correct label_map key)
label_corrections = {
    "Stop Sign": "sign_stop",
    "No Entry Sign": "sign_noentry",
    "Yield Sign": "sign_yield",
    "Do Not Enter": "sign_noentry",
    "One Way Left": "sign_oneway_left",
    "One Way Right": "sign_oneway_right"
}

def determine_one_way_sign(filename):
    """Assign correct One Way Sign direction based on team01 file numbers."""
    match = re.match(r"team01_(\d+)", filename)
    if match:
        file_number = int(match.group(1))
        if 52 <= file_number <= 60:
            return "sign_oneway_right"
        elif 62 <= file_number <= 79:
            return "sign_oneway_left"
    return None  # If not in the range, don't change it

def clean_and_fix_labels():
    corrections_made = 0  # Counter for corrected labels
    for xml_file in os.listdir(ANNOTATION_DIR):
        if not xml_file.endswith(".xml"):
            continue  # Skip non-XML files

        xml_path = os.path.join(ANNOTATION_DIR, xml_file)
        tree = ET.parse(xml_path)
        root = tree.getroot()
        modified = False  # Track if changes are made

        # Iterate through all objects in the XML file
        for obj in root.findall("object"):
            name_tag = obj.find("name")
            if name_tag is not None:
                original_name = name_tag.text.strip()  # Remove tabs, spaces, newlines

                # Handle "One Way Sign" for specific team01 files
                if original_name == "One Way Sign":
                    corrected_name = determine_one_way_sign(xml_file)
                    if corrected_name:
                        print(f"Fixing One Way Sign in {xml_file} → {corrected_name}")
                        name_tag.text = corrected_name
                        modified = True
                        corrections_made += 1
                    else:
                        print(f"⚠️ Warning: Found 'One Way Sign' in {xml_file}, but not in range.")

                # Check if label needs correction
                elif original_name in label_corrections:
                    corrected_name = label_corrections[original_name]
                    print(f"Fixing label: '{original_name}' → '{corrected_name}' in {xml_file}")
                    name_tag.text = corrected_name
                    modified = True
                    corrections_made += 1
                elif original_name not in label_corrections.values():
                    print(f"⚠️ Warning: Unrecognized label '{original_name}' in {xml_file}")

        # Save modifications if any labels were fixed
        if modified:
            tree.write(xml_path)
            print(f"✅ Updated {xml_file}")

    print(f"\n🎯 Total corrections made: {corrections_made}")

if __name__ == "__main__":
    clean_and_fix_labels()
    print("\n✅ All object names cleaned and standardized to match label_map!")
