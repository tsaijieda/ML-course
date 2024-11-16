import numpy as np
import matplotlib.pyplot as plt
from pymatgen.core import Structure
from pymatgen.analysis.diffraction.xrd import XRDCalculator

# Load CIF file and generate XRD pattern
structure = Structure.from_file("../rawdata/2002915.cif")
xrd_calc = XRDCalculator()
xrd_pattern = xrd_calc.get_pattern(structure)

# Extract x and y values from XRD data
x_points = np.array(xrd_pattern.x)  # 2θ values
y_points = np.array(xrd_pattern.y)  # Intensity values

# Define a finer x-axis for a continuous range
x_fine = np.linspace(5, 90, 8500)  # Adjust this range as needed

# Define the standard deviation for the Gaussian function
sigma = 0.05  # Adjust sigma for desired smoothing

# Initialize the convolved y values over the continuous x_fine
y_convolved = np.zeros_like(x_fine)

# Perform Gaussian convolution
for i in range(len(x_points)):
    y_convolved += y_points[i] * np.exp(-((x_fine - x_points[i]) ** 2) / (2 * sigma ** 2))

# Plot the original XRD points and the smoothed, continuous curve
#plt.plot(x_points, y_points, 'o', label="Original XRD Points")  # Original points
plt.plot(x_fine, y_convolved, label="Gaussian Convolution", alpha=0.8)  # Convolved curve
#plt.xlabel("2θ (degrees)")
#plt.ylabel("Intensity (a.u.)")
#plt.title("XRD Pattern with Gaussian Convolution")
#plt.legend()
plt.show()

