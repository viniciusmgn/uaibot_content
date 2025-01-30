import os
from PIL import Image

def rotate_image(image_path, degrees):
    """Rotates the image by the given degrees."""
    with Image.open(image_path) as img:
        img = img.rotate(degrees, expand=True)
        img.save(image_path)

def rename_pngs(ldr_name):
    # Define the mapping of old names to new names and required rotations
    rename_map = {
        "ny.png": (f"{ldr_name}_nz.png", None),
        "py.png": (f"{ldr_name}_pz.png", None),
        "nx.png": (f"{ldr_name}_nx.png", -90),
        "pz.png": (f"{ldr_name}_ny.png", None),
        "px.png": (f"{ldr_name}_px.png", 90),
        "nz.png": (f"{ldr_name}_py.png", -180),
    }
    
    # Get the current directory
    current_dir = os.getcwd()
    
    # Check if all expected files exist before renaming
    missing_files = [file for file in rename_map if not os.path.exists(os.path.join(current_dir, file))]
    if missing_files:
        print(f"Warning: The following files are missing and won't be renamed: {missing_files}")
    
    # Rename files safely by first renaming them to temporary names
    temp_map = {file: os.path.join(current_dir, f"temp_{file}") for file in rename_map if os.path.exists(os.path.join(current_dir, file))}
    for old_name, temp_name in temp_map.items():
        os.rename(os.path.join(current_dir, old_name), temp_name)
    
    # Apply final renaming from temporary names to target names, applying rotations if needed
    for old_name, (new_name, rotation) in rename_map.items():
        temp_name = temp_map.get(old_name)
        if temp_name and os.path.exists(temp_name):
            final_path = os.path.join(current_dir, new_name)
            os.rename(temp_name, final_path)
            if rotation is not None:
                rotate_image(final_path, rotation)
    
    print("Renaming and rotation completed successfully.")

# Example usage
ldr_name = "orchard_road"  # Change this to your desired prefix
rename_pngs(ldr_name)

