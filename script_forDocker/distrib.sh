#!/bin/bash

# The script is to streamline the workflow between VMEC, TERPSICHORE, and DCON.
# The paths below are only for docker.
# If not using docker, you have to change all path in every scrips to your own usage.
#
# All scripts here arec reated by Lin Shih
# email: linshih010@gmail.com
#
# 2024/08/09

current_dir=$(pwd)
exe_dir="/workspace/General-tool/script_forDocker"
vmec_path="/workspace/Stellarator-Tools/build/_deps/parvmec-build"
terp_path="/workspace/TERPSICHORE/TERPSICHORE_main"
bsj_path="/workspace/TERPSICHORE/terp_bootsj"

if [ "$current_dir" == "$exe_dir" ]; then

        echo "cp bootsj_quick.sh \
              run_dcon_singlefile.sh \
              terps_quick.sh \
              descur2vmec.py \
              pcurr_generator.py \
              read_netcdf.py 
              vm3_quick.sh to VMEC run directory"
        cp ${current_dir}/bootsj_quick.sh \
           ${current_dir}/run_dcon_singlefile.sh \
           ${current_dir}/terps_quick.sh \
           ${current_dir}/descur2vmec.py \
           ${current_dir}/pcurr_generator.py \
           ${current_dir}/read_netcdf.py \
           ${current_dir}/vm3_quick.sh  \
           ${current_dir}/check_profile.sh \
           ${vmec_path}
        echo "cp fort43_generator.sh to terp_bsj run directory"
        cp ${current_dir}/fort43_generator.sh ${bsj_path}
else
        echo "You are not executable directory"
        echo "Gone to execute dir automatically!"
        cd $exe_dir
fi
