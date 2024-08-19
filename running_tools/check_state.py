import os
import glob
import shutil
import re
import csv
import argparse

def process_output_files(input_directory, stable_directory, unstable_directory, patterns):
    if not os.path.exists(stable_directory):
        os.makedirs(stable_directory)
    if not os.path.exists(unstable_directory):
        os.makedirs(unstable_directory)
    
    stable_results = []

    def move_related_files(identifier, target_directory):
        for pattern in patterns:
            related_files = glob.glob(os.path.join(input_directory, pattern))
            for file_path in related_files:
                file_name = os.path.basename(file_path)
                if re.search(f"_{identifier}(\\.|_)", file_name):
                    target_file_path = os.path.join(target_directory, file_name)
                    shutil.copy(file_path, target_file_path)
                    print(f"Copied '{file_path}' to '{target_file_path}'.")

    output_files = glob.glob(os.path.join(input_directory, "output_*.txt"))
    
    for output_file in output_files:
        file_name = os.path.basename(output_file)
        identifier = re.search(r"output_(FIRST\d+).*\.txt", file_name).group(1)  # Extract identifier, e.g., "FIRST9"
        
        try:
            with open(output_file, 'r', errors='ignore') as file:
                content = file.readlines()
        except Exception as e:
            print(f"Error reading file {output_file}: {e}")
            continue

        # Determine the stability of the results
        if "unstable" in ''.join(content):
            target_directory = unstable_directory
        else:
            target_directory = stable_directory
            
            # Extract the last occurrence of betat, betan, betaj
            for line in reversed(content):
                if re.search(r'betat =\s+[\d.E+-]+,\s+betan =\s+[\d.E+-]+,\s+betaj =\s+[\d.E+-]+', line):
                    match = re.search(r'betat =\s+([\d.E+-]+),\s+betan =\s+([\d.E+-]+),\s+betaj =\s+([\d.E+-]+)', line)
                    betat = match.group(1)
                    betan = match.group(2)
                    betaj = match.group(3)
                    stable_results.append([identifier, betat, betan, betaj])
                    break

        # Move the output file
        new_file_name = f"{file_name}"
        target_file_path = os.path.join(target_directory, new_file_name)
        shutil.copy(output_file, target_file_path)
        print(f"Copied '{output_file}' to '{target_file_path}' as '{new_file_name}'.")

        # Move related files
        move_related_files(identifier, target_directory)

    # Save the results to a CSV file
    with open('stable_results.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Identifier', 'betat', 'betan', 'betaj'])
        csvwriter.writerows(stable_results)

def main():
    parser = argparse.ArgumentParser(description="Process and categorize VMEC output files.")
    parser.add_argument('--input_directory', type=str, required=True, help="Directory where output files are initially stored.")
    parser.add_argument('--stable_directory', type=str, required=True, help="Directory to store stable results.")
    parser.add_argument('--unstable_directory', type=str, required=True, help="Directory to store unstable results.")
    
    args = parser.parse_args()

    # Patterns to match different types of files
    patterns = [
        "output_*.txt", 
        "jxbout_*.nc", 
        "threed1.*", 
        "wout_*.nc", 
        "wout_*.txt", 
        "mercier.*", 
        "dcon_*", 
        "input.*"
    ]

    process_output_files(args.input_directory, args.stable_directory, args.unstable_directory, patterns)
    print("Output files have been processed and categorized into separate folders for stable and unstable results.")

if __name__ == "__main__":
    main()