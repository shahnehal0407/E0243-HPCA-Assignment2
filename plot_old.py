import matplotlib.pyplot as plt
import re

# File path to the regions data file
file_path = 'all_regions_old.txt'

# Lists to hold data
regions = []
l2_misses = []

# Regular expression pattern to extract data
pattern = r'Region \(Hex\): (\S+), Region \(Decimal\): (\d+), L2 Misses: (\d+)'
i = 1
# Reading and parsing the file
with open(file_path, 'r') as file:
    for line in file:
        match = re.match(pattern, line)
        if match:
            region_hex = match.group(1)  # Hexadecimal representation of region
            l2_miss_count = int(match.group(3))  # L2 Misses count
            regions.append(i)
            i += 1
            l2_misses.append(l2_miss_count)

# Create the plot
plt.figure(figsize=(15, 7))

# Plot the solid line for L2 misses
plt.plot(regions, l2_misses, color='red', linewidth=2, linestyle='-', label='L2 Misses')

# Mark points on the solid line with blue dots
plt.scatter(regions, l2_misses, color='blue', s=30, label='Data Points')  # Changed color to blue

# Labeling the graph
plt.xlabel('2MB Virtual Address Regions (Hex)', fontsize=12)
plt.ylabel('Number of L2 Misses', fontsize=12)
plt.title('L2 Misses for 2MB Virtual Address Regions Before Allocating Page', fontsize=14)

# Customize the plot
plt.xticks(rotation=90, fontsize=8)
plt.grid(True, linestyle='--', alpha=0.6)

# Set limits to match the appearance
plt.ylim(min(l2_misses) - 5, max(l2_misses) + 5)

# Add a legend
plt.legend()

# Display the plot
plt.tight_layout()
plt.show()
