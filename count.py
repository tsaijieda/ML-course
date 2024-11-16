import os
import warnings
from pymatgen.core import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from collections import Counter

# Directory containing CIF files
cif_directory = "rawdata"

# Initialize a counter to store the count of each Bravais lattice type
bravais_lattice_count = Counter()

# List to store details of CIF files with warnings or errors
files_with_issues = []

# Iterate over each CIF file in the directory
for i, filename in enumerate(os.listdir(cif_directory)):
    if filename.endswith(".cif"):
        # Load the structure from the CIF file
        cif_path = os.path.join(cif_directory, filename)
        
        # Print progress only for files that are multiples of 1000
        if (i + 1) % 1000 == 0:
            print(f"Processing file {i + 1}: {filename}")

        try:
            # Load the structure and check for warnings
            with warnings.catch_warnings(record=True) as caught_warnings:
                warnings.simplefilter("always")  # Catch all warnings
                structure = Structure.from_file(cif_path)

                # If warnings were caught, add them to the warnings list
                if caught_warnings:
                    warning_msgs = [str(warning.message) for warning in caught_warnings]
                    files_with_issues.append((filename, warning_msgs))

            # Use SpacegroupAnalyzer to determine the lattice system
            sga = SpacegroupAnalyzer(structure)
            lattice_system = sga.get_crystal_system()  # e.g., 'cubic', 'tetragonal', etc.
            
            # Increment the count for the lattice system
            bravais_lattice_count[lattice_system] += 1

        except ValueError as e:
            # Explicitly log the "Invalid CIF file with no structures!" error
            error_msg = str(e)
            files_with_issues.append((filename, [error_msg]))

        except Exception as e:
            # Catch any other unexpected errors
            error_msg = str(e)
            files_with_issues.append((filename, [f"Unexpected error: {error_msg}"]))

# Print the counts for each Bravais lattice group
print("\nBravais lattice counts:")
for lattice, count in bravais_lattice_count.items():
    print(f"{lattice.capitalize()}: {count}")

# Print details of CIF files with warnings or errors
print("\nFiles with issues:")
for filename, issues in files_with_issues:
    print(f"File: {filename}")
    for issue_msg in issues:
        print(f"  Issue: {issue_msg}")

# Optionally, save warnings and errors to a log file
with open("warnings_and_errors.log", "w") as log_file:
    for filename, issues in files_with_issues:
        log_file.write(f"File: {filename}\n")
        for issue_msg in issues:
            log_file.write(f"  Issue: {issue_msg}\n")

