import os

# Directories and files
output_data_dir = "./output_data"
filelist_path = "filelist_for_xrd.txt"

# Ensure the directories and file exist
if not os.path.isdir(output_data_dir):
    raise FileNotFoundError(f"The directory '{output_data_dir}' does not exist.")
if not os.path.isfile(filelist_path):
    raise FileNotFoundError(f"The file '{filelist_path}' does not exist.")

# List all existing .npz files in the output_data directory
output_npz_files = {os.path.splitext(filename)[0].split("_")[0] for filename in os.listdir(output_data_dir) if filename.endswith(".npz")}
print(f"Found {len(output_npz_files)} .npz files in '{output_data_dir}'.")
print(f"NPZ Files: {output_npz_files}")

# Read filelist_for_xrd.txt
with open(filelist_path, "r") as f:
    cif_lines = f.readlines()

print(f"Found {len(cif_lines)} lines in '{filelist_path}'.")

# Filter out CIF files corresponding to existing .npz files
filtered_lines = []
removed_count = 0

for line in cif_lines:
    num = line.strip().split(".")[0]  # Extract the number (e.g., 1010840 from 1010840.cif)
    if num in output_npz_files:
        print(f"Removing: {line.strip()} (matches .npz file)")
        removed_count += 1
    else:
        filtered_lines.append(line)

# Write the filtered lines back to filelist_for_xrd.txt
with open(filelist_path, "w") as f:
    f.writelines(filtered_lines)

print(f"Filtered {removed_count} entries from '{filelist_path}'. Remaining: {len(filtered_lines)}.")

