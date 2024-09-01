import re
import csv
import os
import argparse
import netCDF4 as nc
import numpy as np

mu0 = 4 * np.pi * 1e-7  # 磁導率常數
a = 0.32

def extract_data_from_txt(filename):
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
            results.append((nn, fix_boundary, free_boundary, ballooning, mercier))

    return results

def extract_data_from_nc(nc_file):
    with nc.Dataset(nc_file, 'r') as ds:
        p_avg = ds.variables['p_avg'][:]
        b0 = ds.variables['b0'][:]
        ctor = ds.variables['ctor'][:]
        # 計算 beta 和 beta_N
        betatotal = p_avg * 2 * mu0 / (b0 * b0)
        beta_N = betatotal * 100 * a * np.abs(b0) / (np.abs(ctor) * 1e-6)
        
        print("====================================")
        print(p_avg)
        print(b0)
        print(ctor)
        print(betatotal)
        print(beta_N)
        print("====================================")

    return betatotal, beta_N

def extract_bsc_data(filename):
    bsc = None
    bsc_ratio = None
    
    with open(filename, 'r') as file:
        for line in file:
            stripped_line = line.strip()  # 移除前後的空白字符
            if stripped_line.startswith('!bsc ') and 'ratio' not in stripped_line:
                print(f"Parsing bsc line: {stripped_line}")
                bsc = float(stripped_line.split('=')[1].strip())
            elif 'bsc ratio' in stripped_line:
                print(f"Parsing bsc ratio line: {stripped_line}")
                bsc_ratio = float(stripped_line.split('=')[1].strip())
    
    print(f"Final parsed values - bsc: {bsc}, bsc_ratio: {bsc_ratio}")
    return bsc, bsc_ratio

def write_to_csv(data, output_filepath):
    with open(output_filepath, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['nn', 'Fix boundary', 'All free-boundary modes', 'Ballooning', 'Mercier', 'beta', 'beta_N', 'bsc', 'bsc_ratio'])
        csvwriter.writerows(data)

def process_files_in_directory(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.startswith("output_") and filename.endswith(".txt"):
            # 提取對應的wout文件名稱
            base_name = os.path.splitext(filename)[0].replace("output_", "wout_")
            nc_filename = base_name + ".nc"
            nc_filepath = os.path.join(input_directory, nc_filename)

            # 提取對應的new_profile文件名稱
            new_profile_filename = base_name.replace("wout_", "new_profile_") + ".txt"
            new_profile_filepath = os.path.join(input_directory, new_profile_filename)

            if os.path.exists(nc_filepath):
                filepath = os.path.join(input_directory, filename)
                txt_data = extract_data_from_txt(filepath)
                betatotal, beta_N = extract_data_from_nc(nc_filepath)

                # 提取bsc和bsc ratio
                bsc, bsc_ratio = None, None
                if os.path.exists(new_profile_filepath):
                    bsc, bsc_ratio = extract_bsc_data(new_profile_filepath)
                
                print(bsc)
                print(bsc_ratio)

                # 因為 betatotal 和 beta_N 是標量，所以直接將它們附加到每個 entry
                # complete_data = [(*entry, betatotal, beta_N, bsc, bsc_ratio) for entry in txt_data]
                complete_data = []
                for i, entry in enumerate(txt_data):
                    if i == 0:
                        complete_data.append((*entry, betatotal, beta_N, bsc, bsc_ratio))
                    else:
                        complete_data.append((*entry, None, None, None, None))
                
                output_filename = os.path.splitext(filename)[0] + '.csv'
                output_filepath = os.path.join(output_directory, output_filename)
                write_to_csv(complete_data, output_filepath)
                print(f'Processed {filename} and saved as {output_filepath}')
            else:
                print(f'Corresponding .nc file not found for {filename}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract data from text files and NetCDF files, then write to CSV.")
    parser.add_argument('--input_directory', type=str, required=True, help="Directory containing input text and NetCDF files.")
    parser.add_argument('--output_directory', type=str, required=True, help="Directory to save output CSV files.")

    args = parser.parse_args()

    process_files_in_directory(args.input_directory, args.output_directory)

    print('Data extraction and CSV creation for all files completed.')
