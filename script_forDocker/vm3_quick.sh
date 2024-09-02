#!/bin/bash
#
#  Created by Lin Shih
#  2023/12/11 
#  Only for snake study
#  VMEC -> vmec2tpr -> vm3dp
#  ./vm3_quick <filename> 

inputvmec=${1}
iteration=${2}
vmec_dir=$(pwd)
vmec2tpr_dir="/workspace/TERPSICHORE/vmec2tpr"
bootsj="/workspace/TERPSICHORE/terp_bootsj"
vm3dp_dir='/workspace/TERPSICHORE/vm3dp'


echo "VMEC input namelist: input.${inputvmec} & wout_${inputvmec}.txt"
if [ ! -e "wout_$inputvmec.txt" ]; then
  echo "Error: Input file 'wout_$inputvmec.txt' not found. Exiting script."
  exit 1
fi

ns=$(awk 'NR==3 {print $2}' wout_${inputvmec}.txt)
echo "ns_array from wout.txt: $ns"

echo "Copy wout to fort.8 and run vm2ptr (coordinate transform)"
cp wout_${inputvmec}.txt ${vmec2tpr_dir}
cd ${vmec2tpr_dir}
cp wout_${inputvmec}.txt fort.8
./vmec2terps.x

mv fort.73 ${vm3dp_dir}/fort.23

echo "Recompile vm3dp and Plot snake ..."
cd ${vm3dp_dir}
new_value=$((ns-1))
sed -i "3s/nit=[0-9]*/nit=${new_value}/" plovma.inc
make clean && make
./vm3dbm90.x < vmaplo.dat_snake_n3
cp fort.37 f6snake
cp f6snake f6snake_${inputvmec}

# open MATLAB
# run snake_plot.m
# in matlab

#nturns=5
#[r,v,p]=snake_plot(nturns)

echo "Plot toroidal plan..."

# here is different!
./vm3dbm90.x < vmaplo.data
cp fort.37 f6sph
cp f6sph f6sph_${substring}
