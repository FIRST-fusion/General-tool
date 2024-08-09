#!/bin/bash
#  VMEC -> vmec2tpr -> bootsj
#  Coupled with bootsj_quick.sh
#  Create fort.43, fort.48 for running bootstrap current
#
#
#  Created by Lin Shih
#  2023/12/11 
#

# Total count of 0.00000000E+00 = NS-3
inputname=${1}
value=${2}
iteration=${3}
total_count=$((value-3))

# Function of generator
function generator(){

   # Number of items per line
   per_line=5
   
   # Calculate the number of lines
   line_count=$((total_count / per_line))
   
   # Calculate the remainder for the last line
   remainder=$((total_count % per_line))
   
   # Start generating the file
   echo -n > "$file_name"
   
   # Iterate to generate each line
   for ((i = 0; i < line_count; i++)); do
       echo -n " " >> "$file_name"
       for ((j = 0; j < per_line; j++)); do
           echo -n " 0.00000000E+00 " >> "$file_name"
       done
       echo >> "$file_name"
   done
   
   # Generate the last line
   echo -n " " >> "$file_name"
   for ((i = 0; i < remainder; i++)); do
       echo -n " 0.00000000E+00 " >> "$file_name"
   done
   
   # Check if there's a remainder
   if [[ $remainder != 0 ]]; then
       echo " " >> "$file_name"
       echo -n " " >> "$file_name"
       echo -n " " >> "$file_name"
   else
       echo -n " " >> "$file_name"
   fi
   #cp fort.43 fort.48
   # Display the contents of the generated file
   # cat "$file_name"
}


file="tprbap_modules.f"
#file="test.txt"
echo "> Changing the value of NI in line 8 of $file to $total_count"
sed -i "8s/\(NI=\)[0-9]*/\1$total_count/" "$file"
if [ "$total_count" -lt 0 ]; then
    echo "Error: NI is less than 0. Stopping the script."
    exit 1
fi
cat ${file} | grep NI=

echo "> Recompile after modifying $file"
make clean && make
mkdir -p obj 
mv *.o *.mod obj/

# If iteration number = 1, do this below, otherwise don't change fort.43 
if [ "${iteration}" -eq 1 ]; then

   # Remove existing fort.43 file
   rm fort.43 fort.48 fort.49
   file_name="fort.43"
   generator;   
   cp fort.43 fort.48
   cp fort.43 fort.49

elif [ "${iteration}" -eq 2 ]; then
   if [[ ${inputname} == *_bootsj* ]]; then
     truncated_string="${inputname%%_bootsj*}"
     echo "Truncated string: $truncated_string"
   else
     echo "String does not contain '_bootsj', no truncation needed."
   fi
   cp fort.43_${truncated_string} fort.43
   cp fort.49_${truncated_string} fort.49
   
   file_name="fort.48"
   generator;

else
   # to make tcv_30*_bootsj2 to become tcv_30*_bootsj1
   # grep -oP '\d+$' extracts the numeric part at the end of the string.
   numeric_part=$(echo "$inputname" | grep -oP '\d+$')

   if [[ -n "$numeric_part" ]]; then
       previous_iter=$((numeric_part - 1))
       prev_inputname="${inputname%"$numeric_part"}$previous_iter"
       echo "When iterating input.$inputname, we use the previous result $prev_inputname "
   else
       echo "Error:No numeric part found in the string. Exiting script."
       exit 1
   fi

   cp fort.43_${prev_inputname} fort.43
   cp fort.49_${prev_inputname} fort.49
   
   file_name="fort.48"
   generator;

fi


