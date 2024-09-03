import subprocess
import re
import os
import argparse

prefix_dir = "/workspace/Stellarator-Tools/build/_deps/parvmec-build"

def run_command(command):
    print(f"Executing: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Command failed: {command}\nError: {result.stderr}")
    print(f"Output: {result.stdout}")
    return result.stdout

def get_bsj_fraction(output):
    match = re.search(r"BOOTSTRAP CURRENT: =\s*([-\d\.E+]+)", output)
    if match:
        bsj_fraction = abs(float(match.group(1)))
        return bsj_fraction
    else:
        raise Exception("Could not find BOOTSTRAP CURRENT value in output.")

def get_Itotal(input_filename):
    with open(input_filename, 'r') as file:
        content = file.read()
    match = re.search(r"curtor\s*=\s*([\d\.E+]+)", content)
    if match:
        Itotal = match.group(1)
        return Itotal
    else:
        raise Exception(f"Could not find curtor value in {input_filename}.")

def update_input_file(input_filename, new_profile_filename, output_folder):
    # 讀取原始 input 檔案
    with open(input_filename, 'r') as file:
        lines = file.readlines()

    # 註解掉 'ac' 開頭的行
    updated_lines = []
    for line in lines:
        if line.strip().startswith("ac"):
            updated_lines.append(f"! {line}")
        else:
            updated_lines.append(line)

    # 讀取 new_profile_filename 的內容
    with open(new_profile_filename, 'r') as file:
        new_profile_content = file.read()

    # 將 new_profile_filename 的內容插入到原始 input 檔案中的對應位置
    insert_index = next(i for i, line in enumerate(updated_lines) if line.strip() == "/")
    updated_lines.insert(insert_index, f"{new_profile_content}\n")

    # 生成新的 input 檔案
    os.makedirs(output_folder, exist_ok=True)
    new_input_filename = os.path.join(output_folder, f"{os.path.basename(input_filename)}_bootsj1")
    with open(new_input_filename, 'w') as file:
        file.writelines(updated_lines)

    print(f"New input file created: {new_input_filename}")
    return new_input_filename

def process_input_file(input_filename, output_folder):
    filename = os.path.basename(input_filename).replace("input.", "", 1)

    print(f"Starting process with input file: {input_filename}")

    # 1. 執行 ./xvmec input_filename
    run_command(f"{prefix_dir}/xvmec {input_filename}")

    # 2. 執行 ./bootsj_quick.sh filename 1
    boostj_output = run_command(f"{prefix_dir}/bootsj_quick.sh {filename} 1")

    # 捕捉 bsj_fraction
    bsj_fraction = get_bsj_fraction(boostj_output)
    
    # 捕捉 Itotal
    Itotal = get_Itotal(input_filename)

    # 3. 執行 python3 pcurr_generator.py --bsj bsj_fraction --curtor Itotal --input {filename} --ns 225
    run_command(f"python3 {prefix_dir}/pcurr_generator.py --bsj {bsj_fraction} --curtor {Itotal} --input {filename} --ns 225")

    # 4. 更新 input 檔案
    new_profile_filename = f"new_profile_{filename}.txt"
    new_input_filename = update_input_file(input_filename, new_profile_filename, output_folder)

    # 5. 執行 ./xvmec {new_input_filename}
    # run_command(f"./xvmec {new_input_filename}")

def main():
    parser = argparse.ArgumentParser(description="Process VMEC input files.")
    parser.add_argument('--input_folder', type=str, required=True, help="Folder containing the input files.")
    parser.add_argument('--output_folder', type=str, required=True, help="Folder to save the new input files.")

    args = parser.parse_args()

    input_files = [os.path.join(args.input_folder, f) for f in os.listdir(args.input_folder) if f.startswith("input.")]

    for input_file in input_files:
        process_input_file(input_file, args.output_folder)

if __name__ == "__main__":
    main()
