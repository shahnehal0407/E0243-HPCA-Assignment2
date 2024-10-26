import sys
import subprocess
import re
from collections import defaultdict

def collect_perf_data():
    """Collect memory access traces using perf and return base and end addresses."""
    perf_command = ["perf", "mem", "record", "-o", "perf.data", "--", "make", "run", "SRNO=24623"]
    try:
        # Capture the output of the perf command
        result = subprocess.run(perf_command, capture_output=True, text=True, check=True)

        # Extract base and end addresses from the output
        base_pattern = re.compile(r'Base:\s*(0x[0-9a-fA-F]+)')
        end_pattern = re.compile(r'End:\s*(0x[0-9a-fA-F]+)')

        base_address = base_pattern.search(result.stdout)
        end_address = end_pattern.search(result.stdout)

        if not base_address or not end_address:
            raise ValueError("Base or End address not found in output.")

        return int(base_address.group(1), 16), int(end_address.group(1), 16)

    except subprocess.CalledProcessError as e:
        print(f"Error collecting perf data: {e}")
        sys.exit(1)
    except ValueError as ve:
        print(ve)
        sys.exit(1)

def convert_perf_data():
    """Convert binary perf data to human-readable format."""
    command = ["perf", "mem", "report", "--stdio"]
    try:
        with open("perf_script_output.txt", "w") as outfile:
            subprocess.run(command, stdout=outfile, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error converting perf data: {e}")
        sys.exit(1)


def parse_memory_report_for_l2_misses(file_path, min_address, max_address):
    """Parse memory report to extract L2 misses per 2MB region within specified range."""
    region_l2_misses = defaultdict(int)
    address_pattern = re.compile(r'0x[0-9a-fA-F]+')  # Regex to match hexadecimal addresses

    with open(file_path, 'r') as f:
        for line in f:
            if 'L2 miss' in line:
                match = address_pattern.search(line)
                if match:
                    hex_address = match.group(0)
                    try:
                        address = int(hex_address, 16)
                        if min_address <= address <= max_address:
                            region_base = address >> 21
                            region_l2_misses[region_base] += 1
                    except ValueError:
                        print(f"Warning: Could not convert address {hex_address} in line: {line.strip()}")
                else:
                    print(f"Warning: No valid hexadecimal address found in line: {line.strip()}")

    return region_l2_misses

def find_top_regions(region_l2_misses, n):
    """Find the top N regions with the most L2 misses."""
    sorted_regions = sorted(region_l2_misses.items(), key=lambda x: x[1], reverse=True)
    return sorted_regions[:n]

def save_large_pages(regions, output_file):
    """Save the top regions to a file in decimal format only."""
    with open(output_file, 'w') as f:
        for region, count in regions:
            region_address = region << 21  # Convert to actual address
            f.write(f"{region_address}\n")  # Write only the decimal address

def save_all_regions(region_l2_misses, output_file):
    """Save all regions and their corresponding L2 miss counts to a file."""
    with open(output_file, 'w') as f:
        for region, count in region_l2_misses.items():
            region_address = region << 21
            f.write(f"Region (Hex): {hex(region_address)}, Region (Decimal): {region_address}, L2 Misses: {count}\n")

def main():
    if len(sys.argv) != 2:
        print("Usage: python analyze.py <number_of_large_pages>")
        sys.exit(1)

    # Step 1: Collect perf data and extract base and end address
    min_address, max_address = collect_perf_data()

    # Step 2: Convert perf data to human-readable format
    convert_perf_data()

    # Step 4: Parse the perf output to get L2 miss counts for each 2MB region
    memory_report_path = 'perf_script_output.txt'
    region_l2_misses = parse_memory_report_for_l2_misses(memory_report_path, min_address, max_address)

    # Step 5: Find the top N regions with the most L2 misses
    n = int(sys.argv[1])
    top_regions = find_top_regions(region_l2_misses, n)

    # Step 6: Save the top regions to 'largepages.txt'
    save_large_pages(top_regions, 'largepages.txt')

    # Step 7: Save all regions to 'all_regions.txt'
    # save_all_regions(region_l2_misses, 'all_regions.txt')

if __name__ == "__main__":
    main()
