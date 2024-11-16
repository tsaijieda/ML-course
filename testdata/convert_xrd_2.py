import numpy as np
import os
from pymatgen.core import Structure
from pymatgen.analysis.diffraction.xrd import XRDCalculator
from scipy.stats import truncnorm

# Directory containing CIF files
input_dir = "../rawdata"  # Set this to the directory containing your CIF files
output_dir = "../output_data"  # Directory to save the binary files

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Define x_fine range
x_fine = np.linspace(5, 90, 8500, dtype=np.float32)  # Specify single precision here
sigma = np.random.uniform(0.05, 0.15)  # Standard deviation for Gaussian smoothing

# Process each CIF file
for filename in os.listdir(input_dir):
    if filename.endswith(".cif"):
        filepath = os.path.join(input_dir, filename)
        
        try:
            # Generate new parameters for each file
            T = 0.1 / 3
            mu = T / 3
            sigma = T / 7
            lower, upper = 0, T
            a_trunc, b_trunc = (lower - mu) / sigma, (upper - mu) / sigma
            h = truncnorm.rvs(a_trunc, b_trunc, loc=mu, scale=sigma, size=1)[0]

            # Step function parameters
            a = np.random.uniform(10, 60)
            xu = np.random.uniform(0, 1/7)
            xd = np.random.uniform(6/7, 1)

            # Define step functions
            def f_stepup(x):
                return h * (1 / (1 + np.exp(a * ((x - 5) / 85) - xu)))

            def f_stepdown(x):
                return h * (1 - 1 / (1 + np.exp(a * ((x - 5) / 85) - xd)))

            # Load structure from CIF file and generate XRD pattern
            structure = Structure.from_file(filepath)
            xrd_calc = XRDCalculator()
            xrd_pattern = xrd_calc.get_pattern(structure)
            
            # Extract x and y values
            x_points = np.array(xrd_pattern.x, dtype=np.float32)  # Convert to float32
            y_points = np.array(xrd_pattern.y, dtype=np.float32)  # Convert to float32
            
            # Initialize convolved intensity array
            y_convolved = np.zeros_like(x_fine, dtype=np.float32)  # Convert to float32
            
            # Perform Gaussian convolution
            for i in range(len(x_fine)):
                distance = np.abs(x_fine[i] - x_points)
                close_points_mask = distance < 6 * sigma
                close_x_points = x_points[close_points_mask]
                close_y_points = y_points[close_points_mask]
                gaussian_kernel = np.exp(-((x_fine[i] - close_x_points) ** 2) / (2 * sigma ** 2))
                y_convolved[i] = np.sum(close_y_points * gaussian_kernel)
            
            # Normalize and add noise and step functions
            y_convolved = y_convolved / np.max(y_convolved)
            noise = np.random.uniform(0.002, 0.02, size=y_convolved.shape).astype(np.float32)
            y_convolved = y_convolved + noise + f_stepup(x_fine) + f_stepdown(x_fine)
            
            # Save to a binary .npz file
            output_file = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_convolved.npz")
            np.savez(output_file, x_fine=x_fine, y_convolved=y_convolved)
            print(f"Saved: {output_file}")
        
        except Exception as e:
            print(f"Error processing {filename}: {e}")

