import numpy as np
import matplotlib.pyplot as plt

# Path to the .npz file
file_path = "../output_data/1000071_convolved.npz"

# Load the .npz file
data = np.load(file_path)

# Access the arrays
x_fine = data['x_fine']
y_convolved = data['y_convolved']

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(x_fine, y_convolved, label="Convolved Data", color="blue")
plt.title("XRD Pattern with Convolution", fontsize=14)
plt.xlabel("2θ (degrees)", fontsize=12)
plt.ylabel("Intensity (normalized)", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(fontsize=12)
plt.tight_layout()
plt.show()

