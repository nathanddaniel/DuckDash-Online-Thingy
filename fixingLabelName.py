import os
import xml.etree.ElementTree as ET

# Define the path to your annotations folder
ANNOTATION_DIR = r"C:\Me\Queens\3rd Year\Winter\ELEC 390\DuckDash-Online-Thingy\DuckDash-Online-Thingy\annotations"

# Define the correct label mappings (XML name → label_map key)
label_corrections = {
    "Ducks (Regular)": "duck_regular",
    "Ducks (Specialty)": "duck_specialty",
    "Sign - Stop": "sign_stop",
    "Sign - Oneway Right": "sign_oneway_right",
    "Sign - Oneway Left": "sign_oneway_left",
    "Sign - No Entry": "sign_noentry",
    "Sign - Yield": "sign_yield",
    "Road - Crosswalk": "road_crosswalk",
    "Road - Oneway": "road_oneway",
    "Vehicle": "vehicle"
}

def clean_and_fix_labels():
    for xml_file in os.listdir(ANNOTATION_DIR):
        if not xml_file.endswith(".xml"):
            continue  # Skip non-XML files

        xml_path = os.path.join(ANNOTATION_DIR, xml_file)
        tree = ET.parse(xml_path)
        root = tree.getroot()
        modified = False  # Track changes

        # Iterate through all objects in the XML file
        for obj in root.findall("object"):
            name_tag = obj.find("name")
            if name_tag is not None:
                original_name = name_tag.text.strip()  # Remove tabs, spaces, newlines
                
                # Check if label needs correction
                if original_name in label_corrections:
                    corrected_name = label_corrections[original_name]
                    print(f"Fixing label: '{original_name}' → '{corrected_name}' in {xml_file}")
                    name_tag.text = corrected_name
                    modified = True
                elif original_name not in label_corrections.values():
                    print(f"Warning: Unrecognized label '{original_name}' in {xml_file}")

        # Save modifications if any labels were fixed
        if modified:
            tree.write(xml_path)
            print(f"Updated {xml_file}")

if __name__ == "__main__":
    clean_and_fix_labels()
    print("✅ All object names cleaned and standardized to match label_map!")
