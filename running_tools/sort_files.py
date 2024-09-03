import subprocess
import argparse
import os
import shutil

# prefix_dir = "/workspace/Stellarator-Tools/build/_deps/parvmec-build"
prefix_dir = "/workspace/General-tool/running_tools"

def move_file_using_mv(source_pattern, destination_folder):
    try:
        # Construct the full command string
        command = f"mv {source_pattern} {destination_folder}"
        # Execute the command, allowing the use of shell wildcards
        subprocess.run(command, shell=True, check=True)
        print(f"Files from '{source_pattern}' successfully moved to '{destination_folder}'")
    except subprocess.CalledProcessError as e:
        print(f"Error during move operation: {e}")

def copy_and_rename_files(source_pattern, destination_folder, new_suffix):
    try:
        # List all files matching the source pattern
        files = [f for f in os.listdir(prefix_dir) if f.startswith("new_profile_")]
        for file_name in files:
            # Split the file name into base and extension
            base_name, extension = os.path.splitext(file_name)
            # Create the new file name by appending the suffix before the extension
            new_file_name = f"{base_name}_{new_suffix}{extension}"
            # Full paths for source and destination
            source_file = os.path.join(prefix_dir, file_name)
            destination_file = os.path.join(destination_folder, new_file_name)
            # Copy the file and rename
            shutil.copy2(source_file, destination_file)
            print(f"Copied and renamed '{source_file}' to '{destination_file}'")
    except Exception as e:
        print(f"Error during copy and rename operation: {e}")

def main():
    parser = argparse.ArgumentParser(description="Move VMEC and DCON files.")
    parser.add_argument('--input_directory', type=str, required=True, help="Directory for input files.")
    parser.add_argument('--dcon_directory', type=str, required=True, help="Directory to store DCON files.")
    parser.add_argument('--output_directory', type=str, required=True, help="Directory to move files to.")

    args = parser.parse_args()

    move_file_using_mv(f'{prefix_dir}/jxbout_*_bootsj1*', args.output_directory)
    move_file_using_mv(f'{prefix_dir}/threed1.*_bootsj1*', args.output_directory)
    move_file_using_mv(f'{prefix_dir}/wout_*_bootsj1*', args.output_directory)
    move_file_using_mv(f'{prefix_dir}/mercier.*_bootsj1*', args.output_directory)
    copy_and_rename_files(f'{prefix_dir}/new_profile_*', args.output_directory, 'bootsj1')
    # move_file_using_mv(f'{prefix_dir}/new_profile_*', args.output_directory)
    # move_file_using_cp(f'{args.input_directory}/*', args.output_directory)
    move_file_using_mv(f'{args.dcon_directory}/*', args.output_directory)

if __name__ == "__main__":
    main()
