import os

def rename_pngs(ldr_name):
    # Define the mapping of old names to new names
    rename_map = {
        "ny.png": f"{ldr_name}_nz.png",
        "py.png": f"{ldr_name}_pz.png",
        "nx.png": f"{ldr_name}_nx.png",
        "pz.png": f"{ldr_name}_ny.png",
        "px.png": f"{ldr_name}_px.png",
        "nz.png": f"{ldr_name}_py.png",
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
    
    # Apply final renaming from temporary names to target names
    for old_name, new_name in rename_map.items():
        temp_name = temp_map.get(old_name)
        if temp_name and os.path.exists(temp_name):
            os.rename(temp_name, os.path.join(current_dir, new_name))
    
    print("Renaming completed successfully.")

# Example usage
ldr_name = "outdoors_1"  # Change this to your desired prefix
rename_pngs(ldr_name)

