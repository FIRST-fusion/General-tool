#!/bin/bash
# This script is created by Lin Shih
# Date : 2023 8 12
# After running vmec, execute this script with dcon_{filename}.txt output from vmec
#
#       ./run_dcon_singlefile.sh dcon_{filename}.txt
#
# The script will examine the stability from n = 1 to n = 5 mode.
# You can change the mode range in the forloop.
# Note:
#  Before you run this script:
#       i. modify the eq_type from the default one to 'vmec' in "equil.in" inside the dcon_dir
#       ii. modify dcon_dir to your own path of dcon directory
#
# Contact: Lin Shih (linshih010@gmail.com)


equil_file=${1}

# dcon path 
current_dir=$(pwd)
dcon_dir="/workspace/DCON/rundir/Linux"

cp ${equil_file} ${dcon_dir}
cd ${dcon_dir}
echo "befor change path and file >>> "
cat ${dcon_dir}/equil.in | grep eq_filename
filename=$(basename "$equil_file")
sed -i "s|eq_filename=.*|eq_filename=\"${filename}\"|" ${dcon_dir}/equil.in
#sed -i "s|eq_filename=.*|eq_filename=\"${current_dir}\/${equil_file}\"|" ${dcon_dir}/equil.in

echo "after change path and file >>> "
cat ${dcon_dir}/equil.in | grep eq_filename

echo "Examine mode n = 1 to 3"
for n in {1..3}
do
	sed -i "s|nn=.*|nn=${n}|" ${dcon_dir}/dcon.in
	./dcon 
	echo "---------------------------------------------"
done


# Run "dcon" with the current file as an argument
#./xdraw dcon


