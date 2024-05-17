import subprocess

def move_file_using_mv(source_pattern, destination_folder):
    try:
        # Construct the full command string
        command = f"mv {source_pattern} {destination_folder}"
        # Execute the command, allowing the use of shell wildcards
        subprocess.run(command, shell=True, check=True)
        print(f"Files from '{source_pattern}' successfully moved to '{destination_folder}'")
    except subprocess.CalledProcessError as e:
        print(f"Error during move operation: {e}")

input_directory = "./input_files"  # Directory for input files
dcon_directory = "./dcon_files"  # Directory to store dcon files
move_file_using_mv('./jxbout_*', './output_files')
move_file_using_mv('./threed1.*', './output_files')
move_file_using_mv('./wout_*', './output_files')
move_file_using_mv('./mercier.*', './output_files')
# move_file_using_cp(f'{input_directory}/*', './output_files')
# move_file_using_cp(f'{dcon_directory}/*', './output_files')
