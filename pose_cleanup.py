import os
import xml.etree.ElementTree as ET

# Define the directory containing annotation XML files
ANNOTATION_DIR = r"C:\Me\Queens\3rd Year\Winter\ELEC 390\DuckDash-Online-Thingy\DuckDash-Online-Thingy\annotations"

def fix_missing_pose():
    for xml_file in os.listdir(ANNOTATION_DIR):
        if not xml_file.endswith(".xml"):
            continue  # Skip non-XML files

        xml_path = os.path.join(ANNOTATION_DIR, xml_file)
        tree = ET.parse(xml_path)
        root = tree.getroot()
        modified = False  # Track if changes are made

        # Iterate through all objects in the XML file
        for obj in root.findall("object"):
            pose = obj.find("pose")
            if pose is None:
                # Add missing <pose> tag with value "Unspecified"
                pose_tag = ET.Element("pose")
                pose_tag.text = "Unspecified"
                obj.insert(1, pose_tag)  # Insert after <name> tag
                modified = True

        # Save modifications if any <pose> tags were added
        if modified:
            tree.write(xml_path)
            print(f"Fixed missing <pose> in {xml_file}")

if __name__ == "__main__":
    fix_missing_pose()
    print("✅ All missing <pose> tags have been fixed!")
