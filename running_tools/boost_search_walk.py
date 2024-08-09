import subprocess
import re
import os

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
    new_input_filename = os.path.join(output_folder, f"{os.path.basename(input_filename)}_boostj1")
    with open(new_input_filename, 'w') as file:
        file.writelines(updated_lines)

    print(f"New input file created: {new_input_filename}")
    return new_input_filename

def process_input_file(input_filename, output_folder):
    filename = os.path.basename(input_filename).replace("input.", "", 1)

    print(f"Starting process with input file: {input_filename}")

    # 1. 執行 ./xvmec input_filename
    run_command(f"./xvmec {input_filename}")

    # 2. 執行 ./boostj_quick.sh filename 1
    boostj_output = run_command(f"./boostj_quick.sh {filename} 1")

    # 捕捉 bsj_fraction
    bsj_fraction = get_bsj_fraction(boostj_output)
    
    # 捕捉 Itotal
    Itotal = get_Itotal(input_filename)

    # 3. 執行 ./pcurr_generator.py --bsj bsj_fraction --curtor Itotal --input {filename} --ns 225
    run_command(f"./pcurr_generator.py --bsj {bsj_fraction} --curtor {Itotal} --input {filename} --ns 225")

    # 4. 更新 input 檔案
    new_profile_filename = f"new_profile_{filename}.txt"
    new_input_filename = update_input_file(input_filename, new_profile_filename, output_folder)

    # 5. 執行 ./xvmec {new_input_filename}
    # run_command(f"./xvmec {new_input_filename}")

def main():
    input_folder = "/home/f74091247/Stellarator-Tools/build/_deps/parvmec-build/input_files_0716"  # 指定包含input檔案的資料夾
    output_folder = "/home/f74091247/Stellarator-Tools/build/_deps/parvmec-build/new_input_0716"  # 指定儲存new input檔案的資料夾
    input_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.startswith("input.")]

    for input_file in input_files:
        process_input_file(input_file, output_folder)

if __name__ == "__main__":
    main()
