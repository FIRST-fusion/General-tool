import os

# 設定輸出資料夾
output_directory = "./input_files_0716"  
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# 模板
base_template =  """
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
ns_array = 225,
ftol_array = 1.0e-15,
!ns_array = 49, 81, 121, 225,
!ftol_array = 1.0e-7,1.0e-9, 1.0e-11, 1.0e-15,
SPRES_PED = 1.0,

! Fitting parameters.
GAMMA = 0.0,
PHIEDGE = -0.8
BLOAT = 1.0,
!Enter major radius (R0)     : 0.45
!Enter aspect ratio (epsilon): 1.4
!Enter elongation (kappa)    : 2.4
!Enter triangularity (delta) : 0.5
!Enter number of points      : 100

 RAXIS =  3.761E-01, ZAXIS = -1.776E-17
  RBC(0,0) =   3.792768E-01   , ZBS(0,0) =   0.000000E+00
  RBC(0,1) =   3.173777E-01   , ZBS(0,1) =   7.612256E-01
  RBC(0,2) =   7.008050E-02   , ZBS(0,2) =  -8.807920E-03
  RBC(0,3) =   3.251705E-03   , ZBS(0,3) =  -8.731308E-03
  RBC(0,4) =   6.691509E-04   , ZBS(0,4) =   4.261375E-03
  RBC(0,5) =   8.459768E-04   , ZBS(0,5) =   7.070216E-04
  RBC(0,6) =  -6.855647E-05   , ZBS(0,6) =  -6.410187E-04
  RBC(0,7) =  -4.823187E-05   , ZBS(0,7) =   8.440305E-05
  RBC(0,8) =   5.814622E-05   , ZBS(0,8) =   1.229844E-04
  RBC(0,9) =  -4.688419E-08   , ZBS(0,9) =  -4.849090E-05
  RBC(0,10) =  -1.213299E-05   , ZBS(0,10) =  -1.442473E-05
  RBC(0,11) =   4.993245E-06   , ZBS(0,11) =   1.671574E-05
  RBC(0,12) =   5.525981E-07   , ZBS(0,12) =   5.525981E-07
  RBC(0,13) =  -3.004605E-06   , ZBS(0,13) =  -3.004605E-06
! plasma current parameters.
ncurr = 1,
curtor = 1.50E+06,
! 2(1-s^7)^2-(1-s^3)^2
!ac = 1.0 0.0 0.0 2.0 0.0 0.0 -1.0 -4.0 0.0 0.0 0.0 0.0 0.0 0.0 2.0,
! 2(1-s^10)^2-(1-s^4)^2 
ac = 1.0 0.0 0.0 0.0 2.0 0.0 0.0 0.0 -1.0 0.0 -4.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 2.0
! plasma pressure parameters.
spres_ped = 1.0,
pres_scale = {pres_scale}
am  = 1.0000   -0.3639   0    0   -3.5480    2.9112

/
&END
"""

# 設定 curtor 和 pres_scale 的範圍和步長
curtor_range = range(800000, 800001, 1000)  # 100000 to 200000 with step 10000
pres_scale_range = range(80000, 90001, 200)  # 1000 to 3000 with step 1000

file_index = 1
for curtor in curtor_range:
    for pres_scale in pres_scale_range:
        file_name = f"input.FIRST{file_index}_0716"
        file_path = os.path.join(output_directory, file_name)
        with open(file_path, 'w') as file:
            file_content = base_template.format(curtor=curtor, pres_scale=pres_scale)
            file.write(file_content)
            file_index += 1

print(f"Generated {file_index - 1} files in '{output_directory}'.")
