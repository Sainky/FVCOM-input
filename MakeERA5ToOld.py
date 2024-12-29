# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 10:56:23 2024

@author: X.Zhou @SKLEC (Sh. CN) & NIVA (Bgn. NOR)
"""
# deal with ERA5 atomosphere field variables
# prepare to tran2wind
from netCDF4 import Dataset as nc
import os
from datetime import datetime, timedelta
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt 
from mpl_toolkits.basemap import Basemap
import numpy as np
import cmocean.cm as cm
import warnings
warnings.filterwarnings("ignore")

#ncf1 & ncf2 are unziped ERA5T
newf_i = r'D:\public\data_stream-oper_stepType-instant.nc'
newf_a = r'D:\public\data_stream-oper_stepType-accum.nc'
oldf = r'D:\public\ecmwf.nc'

ncf_i = nc(newf_i)
ncf_a = nc(newf_a)
lon = ncf_i.variables['longitude'][:]
lat = ncf_i.variables['latitude'][:]
time_i = ncf_i.variables['valid_time'][:]
time_a = ncf_a.variables['valid_time'][:]
if not np.array_equal(time_i, time_a):
    raise ValueError("Error: The two arrays are not equal!")


#lonx,laty = np.meshgrid(lon,lat)
#wind
u10 = ncf_i.variables['u10'][:]
v10 = ncf_i.variables['v10'][:]
msl = ncf_i.variables['msl'][:]
#heat radiation
d2m = ncf_i.variables['d2m'][:]
t2m = ncf_i.variables['t2m'][:]
tcc = ncf_i.variables['tcc'][:]
e = ncf_a.variables['e'][:]
#fal = ncf.variables['fal'][:]
slhf = ncf_a.variables['slhf'][:]
sshf = ncf_a.variables['sshf'][:]
ssr = ncf_a.variables['ssr'][:]
sntr = ncf_a.variables['str'][:]
strd = ncf_a.variables['strd'][:]
tp = ncf_a.variables['tp'][:]

ncf_i.close()
ncf_a.close()
#t_str = [str(t[i],encoding = 'utf-8') for i in range(len(t))]
#day = [dt.strptime(i,'%Y-%m-%d_%H:%M:%S') for i in t_str]


#%% save to netCDF file
#convert validtime to era5 hours since 1900-1-1 format
base_1900 = datetime(1900, 1, 1)
base_1970 = datetime(1970, 1, 1)
seconds_offset = (base_1970 - base_1900).total_seconds()
hours_since_1900 = (time_i + seconds_offset) / 3600
time_new = np.array(hours_since_1900)
dates = [base_1900 + timedelta(hours=hours) for hours in hours_since_1900]
print('start from',dates[0],'to',dates[-1])

#os.system('copy '+fnam+' '+'IDL_wind_heat.nc')
#write a standard ERA5 netCDF4 File for coversion
ncf2 = nc(oldf,'w',format='NETCDF4')# format='NETCDF3_CLASSIC')
ncf2.createDimension('time', len(time_new))
ncf2.createDimension('longitude', len(lon))
ncf2.createDimension('latitude',len(lat))

ncf2lon = ncf2.createVariable('longitude', 'f4', ('longitude'))
ncf2lon.units = "degrees_east"
ncf2lon.long_name = "longitude"
ncf2lon[:] = lon[:]

ncf2lat = ncf2.createVariable('latitude', 'f4', ('latitude'))
ncf2lat.units = "degrees_north"
ncf2lat.long_name = "latitude"
ncf2lat[:] = lat[:]

ncf2time = ncf2.createVariable('time', 'i4', ('time'))
ncf2time.units = "hours since 1900-01-01 00:00:00.0"
ncf2time.long_name = "time"
ncf2time.calendar = "gregorian"
ncf2time[:] = time_new[:]
#wind
ncf2u10 = ncf2.createVariable('u10', 'f4', ('time','latitude','longitude'), fill_value=np.int16(-32767))
ncf2u10.scale_factor = 9.271100343320589E-4
ncf2u10.add_offset = -0.8762493826538847
ncf2u10.missing_value = np.int16(-32767)
ncf2u10.units = "m s**-1"
ncf2u10.long_name = "10 metre U wind component"
ncf2u10[:] = u10[:]

ncf2v10 = ncf2.createVariable('v10', 'f4', ('time','latitude','longitude'), fill_value=np.int16(-32767))
ncf2v10.scale_factor = 9.264422454771117E-4
ncf2v10.add_offset = 1.632982518623355
ncf2v10.missing_value = np.int16(-32767)
ncf2v10.units = "m s**-1"
ncf2v10.long_name = "10 metre V wind component"
ncf2v10[:] = v10[:]

#heat radiation
ncf2var = ncf2.createVariable('d2m', 'f4', ('time','latitude','longitude'), fill_value=np.int16(-32767))
ncf2var.scale_factor = 6.639665321288511E-4
ncf2var.add_offset = 282.18667973548395
ncf2var.missing_value = np.int16(-32767)
ncf2var.units = "K"
ncf2var.long_name = "2 metre dewpoint temperature"
ncf2var[:] = d2m[:]
del ncf2var

ncf2var = ncf2.createVariable('e', 'f4', ('time','latitude','longitude'), fill_value=np.int16(-32767))
ncf2var.scale_factor = 2.4057367571191572E-8
ncf2var.add_offset = -5.225148431033532E-4
ncf2var.missing_value = np.int16(-32767)
ncf2var.units = "m of water equivalent"
ncf2var.long_name = "Evaporation"
ncf2var.standard_name = "lwe_thickness_of_water_evaporation_amount"
ncf2var[:] = e[:]
del ncf2var
'''
ncf2var = ncf2.createVariable('fal', 'f4', ('time','latitude','longitude'), fill_value=np.int16(-32767))
ncf2var.scale_factor = 3.3791947252570347E-6
ncf2var.add_offset = 0.17070808243811691
ncf2var.missing_value = np.int16(-32767)
ncf2var.units = "(0 - 1)"
ncf2var.long_name = "Forecast albedo"
ncf2var[:] = flmfal[:]
del ncf2var
'''
ncf2var = ncf2.createVariable('msl', 'f4', ('time','latitude','longitude'), fill_value=np.int16(-32767))
ncf2var.scale_factor = 0.11356873636183297
ncf2var.add_offset = 98640.50571563182
ncf2var.missing_value = np.int16(-32767)
ncf2var.units = "Pa"
ncf2var.long_name = "Mean sea level pressure"
ncf2var.standard_name = "air_pressure_at_mean_sea_level"
ncf2var[:] = msl[:]
del ncf2var

ncf2var = ncf2.createVariable('slhf', 'f4', ('time','latitude','longitude'), fill_value=np.int16(-32767))
ncf2var.scale_factor = 60.16240672638213
ncf2var.add_offset = -1306682.5812033631
ncf2var.missing_value = np.int16(-32767)
ncf2var.units = "J m**-2"
ncf2var.long_name = "Surface latent heat flux"
ncf2var.standard_name = "surface_upward_latent_heat_flux"
ncf2var[:] = slhf[:]
del ncf2var

ncf2var = ncf2.createVariable('sshf', 'f4', ('time','latitude','longitude'), fill_value=np.int16(-32767))
ncf2var.scale_factor = 52.84240001220759
ncf2var.add_offset = -330337.9212000061
ncf2var.missing_value = np.int16(-32767)
ncf2var.units = "J m**-2"
ncf2var.long_name = "Surface sensible heat flux"
ncf2var.standard_name = "surface_upward_sensible_heat_flux"
ncf2var[:] = sshf[:]
del ncf2var

ncf2var = ncf2.createVariable('ssr', 'f4', ('time','latitude','longitude'), fill_value=np.int16(-32767))
ncf2var.scale_factor = 53.201654128454365
ncf2var.add_offset = 1743205.3991729359
ncf2var.missing_value = np.int16(-32767)
ncf2var.units = "J m**-2"
ncf2var.long_name = "Surface net short-wave (solar) radiation"
ncf2var.standard_name = "surface_net_downward_shortwave_flux"
ncf2var[:] = ssr[:]
del ncf2var

ncf2var = ncf2.createVariable('str', 'f4', ('time','latitude','longitude'), fill_value=np.int16(-32767))
ncf2var.scale_factor = 13.822146857308532
ncf2var.add_offset = -360960.28607342864
ncf2var.missing_value = np.int16(-32767)
ncf2var.units = "J m**-2"
ncf2var.long_name = "Surface net long-wave (thermal) radiation"
ncf2var.standard_name = "surface_net_upward_longwave_flux"
ncf2var[:] = sntr[:]
del ncf2var

ncf2var = ncf2.createVariable('strd', 'f4', ('time','latitude','longitude'), fill_value=np.int16(-32767))
ncf2var.scale_factor = 15.07416969313170
ncf2var.add_offset = 1297956.6816651535
ncf2var.missing_value = np.int16(-32767)
ncf2var.units = "J m**-2"
ncf2var.long_name = "Surface long-wave (thermal) radiation downwards"
ncf2var[:] = strd[:]
del ncf2var

ncf2var = ncf2.createVariable('t2m', 'f4', ('time','latitude','longitude'), fill_value=np.int16(-32767))
ncf2var.scale_factor = 6.624279168033662E-4
ncf2var.add_offset = 294.1626326532291
ncf2var.missing_value = np.int16(-32767)
ncf2var.units = "K"
ncf2var.long_name = "2 metre temperature"
ncf2var[:] = t2m[:]
del ncf2var

ncf2var = ncf2.createVariable('tcc', 'f4', ('time','latitude','longitude'), fill_value=np.int16(-32767))
ncf2var.scale_factor = 1.525948758640685E-5
ncf2var.add_offset = 0.4999923702562068
ncf2var.missing_value = np.int16(-32767)
ncf2var.units = "(0 - 1)"
ncf2var.long_name = "Total cloud cover"
ncf2var.standard_name = "cloud_area_fraction"
ncf2var[:] = tcc[:]
del ncf2var

ncf2var = ncf2.createVariable('tp', 'f4', ('time','latitude','longitude'), fill_value=np.int16(-32767))
ncf2var.scale_factor = 6.794745778054449E-7
ncf2var.add_offset = 0.022263664016373207
ncf2var.missing_value = np.int16(-32767)
ncf2var.units = "m"
ncf2var.long_name = "Total precipitation"
ncf2var[:] = tp[:]
del ncf2var

ncf2.close()