import os
import csv
from pymatgen.core import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

# Directories and output file
input_dir = "../rawdata"  # Directory containing the CIF files
output_file = "structure_info.csv"  # Output file to save the extracted data

# Open the output file for writing
with open(output_file, mode="w", newline="") as csv_file:
    # Create a CSV writer object
    csv_writer = csv.writer(csv_file)
    
    # Write the header row
    csv_writer.writerow([
        "filename", "cell_structure", "symmetry_number",
        "space_group_name_Hall", "space_group_name_H-M",
        "cell_angle_alpha", "cell_angle_beta", "cell_angle_gamma",
        "cell_length_a", "cell_length_b", "cell_length_c"
    ])

    # Sort filenames in the directory
    filenames = sorted([f for f in os.listdir(input_dir) if f.endswith(".cif")])

    # Initialize a counter
    processed_count = 0

    # Process each CIF file in sorted order
    for filename in filenames:
        filepath = os.path.join(input_dir, filename)
        try:
            # Load the structure from the CIF file
            structure = Structure.from_file(filepath)
            
            # Get space group information
            analyzer = SpacegroupAnalyzer(structure)
            space_group = analyzer.get_space_group_operations()
            
            # Extract structural information
            lattice = structure.lattice
            data = [
                filename,
                analyzer.get_crystal_system(),
                space_group.int_number,
                space_group.int_symbol,
                analyzer.get_space_group_symbol(),  # Get Hermann-Mauguin name
                round(lattice.alpha, 3),
                round(lattice.beta, 3),
                round(lattice.gamma, 3),
                round(lattice.a, 3),
                round(lattice.b, 3),
                round(lattice.c, 3)
            ]

            # Write the data to the CSV file
            csv_writer.writerow(data)

        except Exception as e:
            print(f"Error processing {filename}: {e}")
        
        # Increment the counter and print progress for every 1000 files processed
        processed_count += 1
        if processed_count % 1000 == 0:
            print(f"Processed {processed_count} files...")

# Final progress message
print(f"Processing complete. Total files processed: {processed_count}")

