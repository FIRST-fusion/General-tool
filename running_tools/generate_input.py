import os

# 設定輸出資料夾
output_directory = "./input_files"  
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# 模板
base_template = """
&INDATA
! VMEC execution parameters.
LFORBAL = F,
LFREEB = F,
DELT = 1.0,
TCON0 = 2.0,
NFP = 1,
NITER = 25000,
NSTEP = 250,
NTOR = 0, 
MPOL = 14,
NZETA = 1,
NVACSKIP = 9,
LASYM = F,
ns_array = 25,
ftol_array = 1.0e-7,
SPRES_PED = 1.0,

! Fitting parameters.
GAMMA = 0.0,
PHIEDGE = -0.07
BLOAT = 1.0,

RAXIS =  3.810E-01, ZAXIS =  1.325E-17
RBC(0,0) =   3.835599E-01   , ZBS(0,0) =   0.000000E+00
RBC(0,1) =   2.960100E-01   , ZBS(0,1) =   6.512330E-01
RBC(0,2) =   6.575528E-02   , ZBS(0,2) =  -6.344648E-03
RBC(0,3) =   3.223871E-03   , ZBS(0,3) =  -7.609341E-03
RBC(0,4) =   7.029564E-04   , ZBS(0,4) =   3.803289E-03
RBC(0,5) =   8.025993E-04   , ZBS(0,5) =   6.013849E-04
RBC(0,6) =  -5.893436E-05   , ZBS(0,6) =  -5.534771E-04
RBC(0,7) =  -3.631119E-05   , ZBS(0,7) =   8.868895E-05
RBC(0,8) =   5.397943E-05   , ZBS(0,8) =   1.024970E-04
RBC(0,9) =  -1.395311E-06   , ZBS(0,9) =  -4.434853E-05
RBC(0,10) =  -1.022966E-05   , ZBS(0,10) =  -9.643125E-06
RBC(0,11) =   4.757725E-06   , ZBS(0,11) =   1.449069E-05
RBC(0,13) =  -2.494667E-06   , ZBS(0,13) =  -2.494667E-06

! Plasma current parameters.
NCURR = 1,
curtor = {curtor:.1E},
ac = 1.0 0.0 2.0 0.0 -5.0 0.0 0.0 0.0 2.0, !j5

! Plasma pressure parameters.
SPRES_PED = 1.0,
pmass_type = 'two_power',
pres_scale = {pres_scale},
am = 1.0 5.0 10.0

/
&END
"""

# 設定 curtor 和 pres_scale 的範圍和步長
curtor_range = range(100000, 200001, 10000)  # 100000 to 200000 with step 10000
pres_scale_range = range(1000, 3001, 1000)  # 1000 to 3000 with step 1000

file_index = 1
for curtor in curtor_range:
    for pres_scale in pres_scale_range:
        file_name = f"input.FIRST{file_index}"
        file_path = os.path.join(output_directory, file_name)
        with open(file_path, 'w') as file:
            file_content = base_template.format(curtor=curtor, pres_scale=pres_scale)
            file.write(file_content)
            file_index += 1

print(f"Generated {file_index - 1} files in '{output_directory}'.")
