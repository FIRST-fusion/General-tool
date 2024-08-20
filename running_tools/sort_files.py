import subprocess
import argparse

prefix_dir = "/workspace/Stellarator-Tools/build/_deps/parvmec-build"

def move_file_using_mv(source_pattern, destination_folder):
    try:
        # Construct the full command string
        command = f"mv {source_pattern} {destination_folder}"
        # Execute the command, allowing the use of shell wildcards
        subprocess.run(command, shell=True, check=True)
        print(f"Files from '{source_pattern}' successfully moved to '{destination_folder}'")
    except subprocess.CalledProcessError as e:
        print(f"Error during move operation: {e}")

def main():
    parser = argparse.ArgumentParser(description="Move VMEC and DCON files.")
    parser.add_argument('--input_directory', type=str, required=True, help="Directory for input files.")
    parser.add_argument('--dcon_directory', type=str, required=True, help="Directory to store DCON files.")
    parser.add_argument('--output_directory', type=str, required=True, help="Directory to move files to.")

    args = parser.parse_args()

    move_file_using_mv(f'{prefix_dir}/jxbout_*', args.output_directory)
    move_file_using_mv(f'{prefix_dir}/threed1.*', args.output_directory)
    move_file_using_mv(f'{prefix_dir}/wout_*', args.output_directory)
    move_file_using_mv(f'{prefix_dir}/mercier.*', args.output_directory)
    # move_file_using_cp(f'{args.input_directory}/*', args.output_directory)
    move_file_using_mv(f'{args.dcon_directory}/*', args.output_directory)

if __name__ == "__main__":
    main()
