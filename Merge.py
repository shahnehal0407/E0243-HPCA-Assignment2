import matplotlib.pyplot as plt
import re

# Function to read data from a file
def read_data(file_path):
    regions = []
    l2_misses = []
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
    
    return regions, l2_misses

# File paths for the two input files
file_path1 = 'all_regions.txt'       # Red area
file_path2 = 'all_regions_old.txt'   # Blue area

# Read data from both files
regions1, l2_misses1 = read_data(file_path1)
regions2, l2_misses2 = read_data(file_path2)

# Define the split point for the transition between solid and semi-transparent fill
split_index1 = len(regions1) // 2  # Midpoint for the first dataset
split_index2 = len(regions2) // 2  # Midpoint for the second dataset

# Create the plot
plt.figure(figsize=(15, 7))

# Plot area for the first file in red:
# Solid fill for the first half
plt.fill_between(regions1, l2_misses1, color='red', where=[x < split_index1 for x in range(len(regions1))], label='After allocation Misses')
# Transparent fill for the second half
plt.fill_between(regions1, l2_misses1, color='red', where=[x >= split_index1 for x in range(len(regions1))])

# Plot area for the second file in blue:
# Solid fill for the first half
plt.fill_between(regions2, l2_misses2, color='blue',  where=[x < split_index2 for x in range(len(regions2))], label='Before allocation Misses')
# Transparent fill for the second half
plt.fill_between(regions2, l2_misses2, color='blue',  where=[x >= split_index2 for x in range(len(regions2))])

# Labeling the graph
plt.xlabel('2MB Virtual Address Regions (Hex)', fontsize=12)
plt.ylabel('Number of L2 Misses', fontsize=12)
plt.title('L2 Misses for 2MB Virtual Address Regions After Allocating Page', fontsize=14)

# Customize the plot
plt.xticks(rotation=90, fontsize=8)
plt.grid(True, linestyle='--', alpha=0.6)

# Set limits to ensure a good display
min_l2_misses = min(min(l2_misses1), min(l2_misses2))
max_l2_misses = max(max(l2_misses1), max(l2_misses2))
plt.ylim(min_l2_misses - 5, max_l2_misses + 5)

# Add a legend
plt.legend()

# Display the plot
plt.tight_layout()
plt.show()
