#!/bin/bash
# Created by Lin Shih
# Date 2024 08 29
# Just to check the consistency of profiles between files by eyes


if [ $# -lt 2 ]; then
  echo "Usage: $0 <vmec_input_file> <search_option>"
  echo "<vmec_input_file> = input.filename"
  echo "<search_option> = ac or am"
  exit 1
fi

# Define filenames
input_file="$1"
SEARCH_OPTION="$2"
pcurr_file="/workspace/Stellarator-Tools/build/_deps/parvmec-build/pcurr_generator.py"
bootps_file="/workspace/TERPSICHORE/terp_bootsj/bootps.f"

# Define colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print lines around a specific string in a given file
print_lines_around_string() {
  local filename=$1
  local search_string=$2
  
  # Check if the file exists
  if [ ! -f "$filename" ]; then
    echo "File '$filename' does not exist."
    return
  fi
  # Check if the filename matches the bootps_file
  if [ "$filename" != "$bootps_file" ]; then
    # Get the line number of the first occurrence of the search string in the file
    local line_number=$(grep -nw "$search_string" "$filename" | head -n 1 | cut -d: -f1)
    
    # If the string is not found, return
    if [ -z "$line_number" ]; then
      echo "String '$search_string' not found in file '$filename'."
      return
    fi
    
    # Calculate the range of lines to display
    local start_line=$((line_number))
    local end_line=$((line_number + 5))
    
    # Use awk to print the lines within the range and add colors
    awk -v start="$start_line" -v end="$end_line" -v target="$line_number" -v red="$RED" -v yellow="$YELLOW" -v nc="$NC" 'NR >= start && NR <= end { 
      if (NR == target) 
        printf("%s%4d: %s%s\n", red, NR, $0, nc); 
      else 
        printf("%s%4d: %s%s\n", yellow, NR, $0, nc); 
    }' "$filename"
  else
    # Get all line numbers of the search string in the file
    grep -nw "$search_string" "$filename" | while IFS=: read -r line_number content; do
      # Calculate the range of lines to display
      local start_line=$((line_number ))
      local end_line=$((line_number + 7))
      
      # Use awk to print the lines within the range and add colors
      awk -v start="$start_line" -v end="$end_line" -v target="$line_number" -v red="$RED" -v yellow="$YELLOW" -v nc="$NC" 'NR >= start && NR <= end { 
        if (NR == target) 
          printf("%s%4d: %s%s\n", red, NR, $0, nc); 
        else 
          printf("%s%4d: %s%s\n", yellow, NR, $0, nc); 
      }' "$filename"
    done
  fi
}

# Main logic to check arguments and call the function accordingly
if [ "$SEARCH_OPTION" == "ac" ]; then
  echo "Checking current profile 'ac' in $1 and 'discretise_ohmic_profile' in pcurr_generator.py ..."
  print_lines_around_string "$input_file" "ac"
  print_lines_around_string "$pcurr_file" "discretise_ohmic_profile"

elif [ "$SEARCH_OPTION" == "am" ]; then
  echo "Checking pressure/density profile around 'am' in $1 and 'Density_Profile' in bootps.f..."
  print_lines_around_string "$input_file" "am"
  print_lines_around_string "$bootps_file" "Density_Profile"

else
  echo "Invalid option. Please use 'ac' or 'am'."
  exit 1
fi
