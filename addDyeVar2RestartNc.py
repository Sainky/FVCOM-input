# -*- coding: utf-8 -*-
"""
Created on Thu Sep  4 22:01:27 2025

@author: XZhou @QIMG (QD. CN) & NIVA (Bgn. NOR)
"""

import netCDF4 as nc
import numpy as np


hotstart_file = nc.Dataset(r'E:\FVCOM_out\\hydts_restart_0001.nc', 'r+')

num_time = hotstart_file.dimensions['time'].size  
num_siglay = hotstart_file.dimensions['siglay'].size
num_node = hotstart_file.dimensions['node'].size

dye_var = hotstart_file.createVariable('DYE', 'f8', ('time', 'siglay', 'node'))

# DYE=0.0
dye_var[:] = np.zeros((num_time, num_siglay, num_node)) 

dye_var.long_name = 'dye concentration'
dye_var.units = 'nondimensional'


hotstart_file.close()
