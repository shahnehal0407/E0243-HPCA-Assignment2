import matplotlib.pyplot as plt
import numpy as np

# Data before and after allocation
metrics = [
    "L1-dcache-loads",
    "L1-dcache-load-misses",
    "L1-dcache-stores",
    "LLC-loads",
    "LLC-load-misses",
    "LLC-stores",
    "LLC-store-misses",
    "dTLB-load-misses",
    "dTLB-store-misses",
    "iTLB-load-misses"
]

before = [
    13024910004,  # L1-dcache-loads
    6166967396,   # L1-dcache-load-misses
    11324296,     # L1-dcache-stores
    32343104,     # LLC-loads
    1640252,      # LLC-load-misses
    187941,       # LLC-stores
    6361,         # LLC-store-misses
    6915952597,   # dTLB-load-misses
    49759,        # dTLB-store-misses
    70384         # iTLB-load-misses
]

after = [
    13017908664,  # L1-dcache-loads
    5624197959,   # L1-dcache-load-misses
    7496117,      # L1-dcache-stores
    6159286,      # LLC-loads
    1314282,      # LLC-load-misses
    115095,       # LLC-stores
    3988,         # LLC-store-misses
    4073267978,   # dTLB-load-misses
    29485,        # dTLB-store-misses
    43767         # iTLB-load-misses
]

#import matplotlib.pyplot as plt
import numpy as np

# Data before and after allocation
metrics = [
    "L1-dcache-loads",
    "L1-dcache-load-misses",
    "L1-dcache-stores",
    "LLC-loads",
    "LLC-load-misses",
    "LLC-stores",
    "LLC-store-misses",
    "dTLB-load-misses",
    "dTLB-store-misses",
    "iTLB-load-misses"
]

before = [
    13024910004,  # L1-dcache-loads
    6166967396,   # L1-dcache-load-misses
    11324296,     # L1-dcache-stores
    32343104,     # LLC-loads
    1640252,      # LLC-load-misses
    187941,       # LLC-stores
    6361,         # LLC-store-misses
    6915952597,   # dTLB-load-misses
    49759,        # dTLB-store-misses
    70384         # iTLB-load-misses
]

after = [
    13017908664,  # L1-dcache-loads
    5624197959,   # L1-dcache-load-misses
    7496117,      # L1-dcache-stores
    6159286,      # LLC-loads
    1314282,      # LLC-load-misses
    115095,       # LLC-stores
    3988,         # LLC-store-misses
    4073267978,   # dTLB-load-misses
    29485,        # dTLB-store-misses
    43767         # iTLB-load-misses
]

# Create the bar chart
x = np.arange(len(metrics))  # Label locations
width = 0.35  # Width of the bars

fig, ax = plt.subplots(figsize=(14, 14))

# Plot bars for "before" and "after" data as horizontal bars
bars1 = ax.barh(x - width/2, before, width, label='Before 2MB Allocation', color='red')
bars2 = ax.barh(x + width/2, after, width, label='After 2MB Allocation', color='blue')

# Set the x-axis to logarithmic scale
ax.set_xscale('log')

# Add some text for labels, title, and custom y-axis tick labels, etc.
ax.set_ylabel('Performance Metrics')
ax.set_xlabel('Counts (log scale)')
ax.set_title('Comparison of Performance Metrics Before and After 2MB Huge Page Allocation')
ax.set_yticks(x)
ax.set_yticklabels(metrics)
ax.legend()

# Add value labels next to each bar
def add_labels(bars):
    for bar in bars:
        xval = bar.get_width()
        # Adjust position for the text next to the bar
        ax.text(
            xval * 1.05,  # Position text slightly to the right of the bar
            bar.get_y() + bar.get_height() / 2.0,
            f'{int(xval):,}',  # Format the number with commas
            va='center', ha='left', fontsize=8, color='black'  # Set the text to black for visibility
        )

add_labels(bars1)
add_labels(bars2)

# Adjust layout for better fit
fig.tight_layout()

# Show the plot
plt.show()
