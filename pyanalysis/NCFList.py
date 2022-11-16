
##            DW Standard Python Library

##          Display attributes of NetCDF file

# Daniel Westwood (daniel.westwood@stfc.ac.uk)

# Updates:
#   - Added to standard python library (01/02/2021)

# ------------------- NCFList.py --------------------
from netCDF4 import Dataset
import numpy as np

def listvars(filename,var='',verb=False):
	ncf = Dataset(filename, 'r', format='NETCDF4')
	if var != '':
		for var in ncf.variables:
			ncf_vars = np.array(ncf.variables[var])
			print(var, np.nanmax(ncf_vars), np.nanmin(ncf_vars))
		#for i in range(len(ncf[var])):
			#for j in range(len(ncf[var][0])):
			#print(ncf_vars[i])
	else:
		for var in ncf.variables:
			if verb:
				print(ncf.variables[var])
			else:
				try:
					print('Short:	{},		Long:	{}'.format(var, ncf.variables[var].long_name))
				except:
					print('Short:	{}'.format(var))
	ncf.close()
if __name__ == '__main__':
	print('pyanalysis: NCFList.py')
	listvars(input('Filename: '), input('Var: '), True)
