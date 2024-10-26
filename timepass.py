# Define a function to read, sort, and write the data
def sort_regions_by_tlb_misses(input_file, output_file):
    # Read the data from the input file
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Parse the lines and extract relevant information
    regions = []
    for line in lines:
        parts = line.strip().split()  # Split the line into parts
        if len(parts) >= 2:  # Ensure there are at least two parts
            region_name = parts[0]  # First part: region name
            tlb_misses = int(parts[1])  # Second part: TLB misses (convert to int)
            regions.append((region_name, tlb_misses))

    # Sort the regions by TLB misses (second element of the tuple)
    sorted_regions = sorted(regions, key=lambda x: x[1])

    # Write the sorted data to the output file
    with open(output_file, 'w') as file:
        for region in sorted_regions:
            file.write(f"{region[0]} {region[1]}\n")  # Write each region and its TLB misses

# Specify the input and output file names
input_file = 'all_regions_old.txt'
output_file = 'output.txt'

# Call the function to sort the regions and write to the output file
sort_regions_by_tlb_misses(input_file, output_file)

print("Sorting complete! Sorted data written to output.txt.")
