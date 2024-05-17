import os
import glob
import shutil

def process_output_files(input_directory, stable_directory, unstable_directory, patterns):
    if not os.path.exists(stable_directory):
        os.makedirs(stable_directory)
    if not os.path.exists(unstable_directory):
        os.makedirs(unstable_directory)
    
    def move_related_files(identifier, target_directory):
        for pattern in patterns:
            related_files = glob.glob(os.path.join(input_directory, f"*{identifier}*"))
            for file_path in related_files:
                file_name = os.path.basename(file_path)
                target_file_path = os.path.join(target_directory, file_name)
                shutil.copy(file_path, target_file_path)
                print(f"Copied '{file_path}' to '{target_file_path}'.")

    output_files = glob.glob(os.path.join(input_directory, "output_*.txt"))
    
    for output_file in output_files:
        file_name = os.path.basename(output_file)
        identifier = file_name.split('_')[1].split('.')[0]  # Extract identifier, e.g., "FIRST9"
        
        try:
            with open(output_file, 'r', errors='ignore') as file:
                content = file.read()
        except Exception as e:
            print(f"Error reading file {output_file}: {e}")
            continue

        # Determine the stability of the results
        if "unstable" in content:
            target_directory = unstable_directory
        else:
            target_directory = stable_directory
        
        # Move the output file
        new_file_name = f"{file_name}"
        target_file_path = os.path.join(target_directory, new_file_name)
        shutil.copy(output_file, target_file_path)
        print(f"Copied '{output_file}' to '{target_file_path}' as '{new_file_name}'.")

        # Move related files
        move_related_files(identifier, target_directory)

def main():
    input_directory = "./output_files_backup"  # Directory where output files are initially stored
    stable_directory = "./processed_outputs/stable"  # Directory to store stable results
    unstable_directory = "./processed_outputs/unstable"  # Directory to store unstable results
    
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

    process_output_files(input_directory, stable_directory, unstable_directory, patterns)
    print("Output files have been processed and categorized into separate folders for stable and unstable results.")

if __name__ == "__main__":
    main()
