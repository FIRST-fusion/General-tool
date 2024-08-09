import re
import csv
import os

def extract_data(filename):
    with open(filename, 'r') as file:
        content = file.read()

    pattern = re.compile(
        r'nn =\s*(\d+).*?(Fixed-boundary mode unstable|All free-boundary modes stable|Free-boundary mode unstable).*?'
        r'Ballooning (stable|unstable).*?'
        r'Mercier (stable|unstable)',
        re.DOTALL
    )

    nn_sections = re.split(r'Equilibrium:', content)
    results = []

    for section in nn_sections:
        match = pattern.search(section)
        if match:
            nn = match.group(1)
            free_boundary = 'stable' if 'All free-boundary modes stable' in match.group(2) else 'unstable'
            ballooning = match.group(3)
            mercier = match.group(4)
            fix_boundary = 'unstable' if 'Zero crossing' in section else 'stable'
            results.append((nn, free_boundary, ballooning, mercier, fix_boundary))

    return results

def write_to_csv(data, output_filepath):
    with open(output_filepath, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['nn', 'All free-boundary modes', 'Ballooning', 'Mercier', 'Fix boundary'])
        csvwriter.writerows(data)

def process_files_in_directory(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.startswith("output_") and filename.endswith(".txt"):
            filepath = os.path.join(input_directory, filename)
            data = extract_data(filepath)
            output_filename = os.path.splitext(filename)[0] + '.csv'
            output_filepath = os.path.join(output_directory, output_filename)
            write_to_csv(data, output_filepath)
            print(f'Processed {filename} and saved as {output_filepath}')

if __name__ == '__main__':
    input_directory = '/home/f74091247/Stellarator-Tools/build/_deps/parvmec-build/output_files'
    output_directory = '/home/f74091247/Stellarator-Tools/build/_deps/parvmec-build/csv_files_0716'
    process_files_in_directory(input_directory, output_directory)

    print('Data extraction and CSV creation for all files completed.')
