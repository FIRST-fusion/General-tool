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
ns_array = 49,
ftol_array = 1.0e-11,
SPRES_PED = 1.0,

! Fitting parameters.
GAMMA = 0.0,
PHIEDGE = -0.12
BLOAT = 1.0,

!Enter major radius (R0)     : 0.45
!Enter aspect ratio (epsilon): 1.4
!Enter elongation (kappa)    : 2.2
!Enter triangularity (delta) : 0.5
!Enter number of points      : 100

 RAXIS =  3.761E-01, ZAXIS = -6.523E-18
  RBC(0,0) =   3.788141E-01   , ZBS(0,0) =   0.000000E+00
  RBC(0,1) =   3.171535E-01   , ZBS(0,1) =   6.977497E-01
  RBC(0,2) =   7.045215E-02   , ZBS(0,2) =  -6.797681E-03
  RBC(0,3) =   3.454265E-03   , ZBS(0,3) =  -8.152984E-03
  RBC(0,4) =   7.532009E-04   , ZBS(0,4) =   4.074913E-03
  RBC(0,5) =   8.598567E-04   , ZBS(0,5) =   6.444428E-04
  RBC(0,6) =  -6.306546E-05   , ZBS(0,6) =  -5.930753E-04
  RBC(0,7) =  -3.887908E-05   , ZBS(0,7) =   9.495307E-05
  RBC(0,8) =   5.794749E-05   , ZBS(0,8) =   1.097509E-04
  RBC(0,9) =  -1.498859E-06   , ZBS(0,9) =  -4.747706E-05
  RBC(0,10) =  -1.087257E-05   , ZBS(0,10) =  -1.034611E-05
  RBC(0,11) =   5.171401E-06   , ZBS(0,11) =   1.543259E-05
  RBC(0,13) =  -2.630055E-06   , ZBS(0,13) =  -2.630055E-06

! Plasma current parameters.
NCURR = 1,
curtor = {curtor:.1E},
ac = 1.0 0.0 2.0 0.0 -5.0 0.0 0.0 0.0 2.0, !j5

! Plasma pressure parameters.
SPRES_PED = 1.0,
pmass_type = 'two_power',
pres_scale = {pres_scale},
am = 1.0 2.3 2.5

/
&END
"""

# 設定 curtor 和 pres_scale 的範圍和步長
curtor_range = range(150000, 200001, 10000)  # 100000 to 200000 with step 10000
pres_scale_range = range(1000, 2001, 100)  # 1000 to 3000 with step 1000

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
