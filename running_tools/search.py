import subprocess
import os
import glob
import argparse

prefix_dir = "/workspace/Stellarator-Tools/build/_deps/parvmec-build"

def run_command(command, input_file, output_path=None):
    try:
        if output_path:
            with open(output_path, 'w') as file:
                result = subprocess.run([command, input_file], check=True, stdout=file, stderr=subprocess.PIPE, text=True)
            print(f"Command '{command} {input_file}' executed successfully, output saved to '{output_path}'")
        else:
            result = subprocess.run([command, input_file], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(f"Command '{command} {input_file}' executed successfully, output as follows:")
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command '{command} {input_file}':")
        print(e.stderr)
        return False  # Return False to indicate the command execution failed
    return True  # Return True to indicate the command execution succeeded

def move_file_using_mv(source_pattern, destination_folder):
    try:
        command = f"mv {source_pattern} {destination_folder}"
        subprocess.run(command, shell=True, check=True)
        print(f"Files from '{source_pattern}' successfully moved to '{destination_folder}'")
    except subprocess.CalledProcessError as e:
        print(f"Error during move operation: {e}")

def move_file_using_cp(source_pattern, destination_folder):
    try:
        command = f"cp {source_pattern} {destination_folder}"
        subprocess.run(command, shell=True, check=True)
        print(f"Files from '{source_pattern}' successfully copied to '{destination_folder}'")
    except subprocess.CalledProcessError as e:
        print(f"Error during copy operation: {e}")

def move_file_using_mv(source, destination):
    try:
        subprocess.run(['mv', source, destination], check=True)
        print(f"File {source} moved to {destination}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Process VMEC and DCON files.")
    parser.add_argument('--input_directory', type=str, required=True, help="Directory for input files.")
    parser.add_argument('--dcon_directory', type=str, required=True, help="Directory to store DCON files.")
    parser.add_argument('--output_directory', type=str, required=True, help="Directory to store output files.")

    args = parser.parse_args()

    if not os.path.exists(args.dcon_directory):
        os.makedirs(args.dcon_directory)
    if not os.path.exists(args.output_directory):
        os.makedirs(args.output_directory)

    input_files = glob.glob(os.path.join(args.input_directory, "input.FIRST*"))

    for input_file in input_files:
        # First command
        if run_command(f"{prefix_dir}/xvmec", input_file):
            # Extract file name from full path and construct corresponding dcon file name
            base_name = os.path.basename(input_file).split('.')[1]  # Extract "FIRST1" from "input.FIRST1"
            dcon_filename = os.path.join("./", f"dcon_{base_name}.txt")
            dcon_target_path = os.path.join(args.dcon_directory, f"dcon_{base_name}.txt")
            output_path = os.path.join(args.output_directory, f"output_{base_name}.txt")

            # Move dcon file to specified directory
            if os.path.exists(dcon_filename):
                os.rename(dcon_filename, dcon_target_path)
                print(f"File: {dcon_filename} moved to {dcon_target_path}")

                # Second command, use new file path and redirect output to file
                run_command("./run_dcon_singlefile.sh", dcon_target_path, output_path=output_path)
            else:
                print(f"File not found: {dcon_filename}")

    move_file_using_mv(f'{prefix_dir}/jxbout_*', args.output_directory)
    move_file_using_mv(f'{prefix_dir}/thread1.*', args.output_directory)
    move_file_using_mv(f'{prefix_dir}/wout_*', args.output_directory)
    move_file_using_mv(f'{prefix_dir}/mercier.*', args.output_directory)
    move_file_using_cp(f'{args.input_directory}/*', args.output_directory)
    move_file_using_cp(f'{args.dcon_directory}/*', args.output_directory)

if __name__ == "__main__":
    main()