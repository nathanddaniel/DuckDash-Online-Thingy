import os
import xml.etree.ElementTree as ET

# Define the path to your annotations folder
ANNOTATION_DIR = r"C:\Me\Queens\3rd Year\Winter\ELEC 390\DuckDash-Online-Thingy\DuckDash-Online-Thingy\annotations"

def fix_bounding_boxes():
    for xml_file in os.listdir(ANNOTATION_DIR):
        if not xml_file.endswith(".xml"):
            continue  # Skip non-XML files

        xml_path = os.path.join(ANNOTATION_DIR, xml_file)
        tree = ET.parse(xml_path)
        root = tree.getroot()
        modified = False  # Track changes

        # Iterate through all objects in the XML file
        for obj in root.findall("object"):
            bndbox = obj.find("bndbox")
            if bndbox is not None:
                for tag in ["xmin", "ymin", "xmax", "ymax"]:
                    tag_element = bndbox.find(tag)
                    if tag_element is not None:
                        try:
                            float_value = float(tag_element.text)  # Convert to float
                            int_value = round(float_value)  # Round to nearest integer
                            tag_element.text = str(int_value)  # Store as string
                            modified = True
                        except ValueError:
                            print(f"Warning: Could not convert {tag_element.text} in {xml_file}")

        # Save modifications if any bounding box values were fixed
        if modified:
            tree.write(xml_path)
            print(f"Fixed bounding box values in {xml_file}")

if __name__ == "__main__":
    fix_bounding_boxes()
    print("✅ All bounding box values converted to integers!")
