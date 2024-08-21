import netCDF4 as nc
import numpy as np

mu0 = 4 * np.pi * 1e-7
a = 0.32 

# Open the NetCDF file
file_path = 'wout_FIRST_test.nc'
ds = nc.Dataset(file_path, 'r')


# Extract a specific variable
p_avg = ds.variables['p_avg'][:]
b0 = ds.variables['b0'][:]
ctor = ds.variables['ctor'][:]
Aminor_p = ds.variables['Aminor_p'][:]
print(f'a = {a}')
print(f'curtor = {ctor}')
print(f'b0 = {b0}')
print(f'p_avg = {p_avg}')
# Calculate beta
betatotal = p_avg * 2 * mu0 / (b0*b0)
beta_N = betatotal *100 * a * np.abs(b0)/ (np.abs(ctor) * 1e-6)

print('')
print(f'beta   = {betatotal}')
print(f'beta_N = {beta_N}')


ds.close()
