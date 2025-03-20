import os
import xml.etree.ElementTree as ET

# Define the path to your annotations folder
ANNOTATION_DIR = r"C:\Me\Queens\3rd Year\Winter\ELEC 390\DuckDash-Online-Thingy\DuckDash-Online-Thingy\annotations"

# Define label map to ensure valid labels
valid_labels = {
    "duck_regular",
    "duck_specialty",
    "sign_stop",
    "sign_oneway_right",
    "sign_oneway_left",
    "sign_noentry",
    "sign_yield",
    "road_crosswalk",
    "road_oneway",
    "vehicle"
}

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
                original_name = name_tag.text.strip()  # Remove extra spaces/tabs/newlines

                if original_name in valid_labels:
                    name_tag.text = original_name  # Ensure it matches exactly
                else:
                    print(f"⚠️ Warning: Unrecognized label '{original_name}' in {xml_file}")

        # Save modifications if any labels were fixed
        if modified:
            tree.write(xml_path)
            print(f"✅ Updated {xml_file}")

    print(f"\n🎯 All labels cleaned and normalized.")

if __name__ == "__main__":
    clean_and_fix_labels()
    print("\n✅ All object names cleaned and standardized to match label_map!")