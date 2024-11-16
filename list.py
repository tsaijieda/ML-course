import os

# Define the directory containing the CIF files
cif_directory = "./rawdata"
output_file = "file_list.txt"

# Ensure the directory exists
if not os.path.isdir(cif_directory):
    raise FileNotFoundError(f"The directory '{cif_directory}' does not exist.")

# Collect all CIF filenames
cif_files = [filename for filename in os.listdir(cif_directory) if filename.endswith(".cif")]

# Write the list of CIF filenames to the text file
with open(output_file, "w") as f:
    for i, filename in enumerate(cif_files):
        f.write(f"{filename}\n")  # Include index for readability

print(f"List of {len(cif_files)} CIF files saved to {output_file}.")

