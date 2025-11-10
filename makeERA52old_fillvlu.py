from netCDF4 import Dataset as nc
import os
from datetime import datetime, timedelta
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# ====================================================
# 输入输出文件路径
# ====================================================
newf_i = r'D:\public\data_stream-oper_stepType-instant.nc'
newf_a = r'D:\public\data_stream-oper_stepType-accum.nc'
oldf = r'D:\public\ecmwf.nc'

# ====================================================
# 打开原 ERA5 文件
# ====================================================
ncf_i = nc(newf_i)
ncf_a = nc(newf_a)
lon = ncf_i.variables['longitude'][:]
lat = ncf_i.variables['latitude'][:]
time_i = ncf_i.variables['valid_time'][:]
time_a = ncf_a.variables['valid_time'][:]
if not np.array_equal(time_i, time_a):
    raise ValueError("Error: The two arrays are not equal!")

# 读取主要变量
u10 = ncf_i.variables['u10'][:]
v10 = ncf_i.variables['v10'][:]
msl = ncf_i.variables['msl'][:]
d2m = ncf_i.variables['d2m'][:]
t2m = ncf_i.variables['t2m'][:]
tcc = ncf_i.variables['tcc'][:]
e = ncf_a.variables['e'][:]
slhf = ncf_a.variables['slhf'][:]
sshf = ncf_a.variables['sshf'][:]
ssr = ncf_a.variables['ssr'][:]
sntr = ncf_a.variables['str'][:]
strd = ncf_a.variables['strd'][:]
tp = ncf_a.variables['tp'][:]

# ====================================================
# 自动读取 FillValue 函数
# ====================================================
def get_fill_value(ncfile, varname, default=-32767):
    """从ERA5文件中读取_FillValue或missing_value"""
    var = ncfile.variables[varname]
    fv = getattr(var, '_FillValue', None)
    if fv is None:
        fv = getattr(var, 'missing_value', default)
    return fv

# ====================================================
# 时间转换为 ERA5 格式（hours since 1900）
# ====================================================
base_1900 = datetime(1900, 1, 1)
base_1970 = datetime(1970, 1, 1)
seconds_offset = (base_1970 - base_1900).total_seconds()
hours_since_1900 = (time_i + seconds_offset) / 3600
time_new = np.array(hours_since_1900)
dates = [base_1900 + timedelta(hours=hours) for hours in hours_since_1900]
print('start from', dates[0], 'to', dates[-1])

# ====================================================
# 写入新的 netCDF 文件
# ====================================================
ncf2 = nc(oldf, 'w', format='NETCDF4')
ncf2.createDimension('time', len(time_new))
ncf2.createDimension('longitude', len(lon))
ncf2.createDimension('latitude', len(lat))

# 坐标变量
ncf2lon = ncf2.createVariable('longitude', 'f4', ('longitude',))
ncf2lon.units = "degrees_east"
ncf2lon.long_name = "longitude"
ncf2lon[:] = lon[:]

ncf2lat = ncf2.createVariable('latitude', 'f4', ('latitude',))
ncf2lat.units = "degrees_north"
ncf2lat.long_name = "latitude"
ncf2lat[:] = lat[:]

ncf2time = ncf2.createVariable('time', 'i4', ('time',))
ncf2time.units = "hours since 1900-01-01 00:00:00.0"
ncf2time.long_name = "time"
ncf2time.calendar = "gregorian"
ncf2time[:] = time_new[:]

# ====================================================
# 主变量写入部分
# ====================================================
# 下面每个变量都自动读取对应的 fill_value
# ====================================================

fv_u10 = get_fill_value(ncf_i, 'u10')
ncf2u10 = ncf2.createVariable('u10', 'f4', ('time','latitude','longitude'), fill_value=fv_u10)
ncf2u10.units = "m s**-1"
ncf2u10.long_name = "10 metre U wind component"
ncf2u10[:] = u10[:]

fv_v10 = get_fill_value(ncf_i, 'v10')
ncf2v10 = ncf2.createVariable('v10', 'f4', ('time','latitude','longitude'), fill_value=fv_v10)
ncf2v10.units = "m s**-1"
ncf2v10.long_name = "10 metre V wind component"
ncf2v10[:] = v10[:]

fv_d2m = get_fill_value(ncf_i, 'd2m')
ncf2var = ncf2.createVariable('d2m', 'f4', ('time','latitude','longitude'), fill_value=fv_d2m)
ncf2var.units = "K"
ncf2var.long_name = "2 metre dewpoint temperature"
ncf2var[:] = d2m[:]
del ncf2var

fv_e = get_fill_value(ncf_a, 'e')
ncf2var = ncf2.createVariable('e', 'f4', ('time','latitude','longitude'), fill_value=fv_e)
ncf2var.units = "m of water equivalent"
ncf2var.long_name = "Evaporation"
ncf2var.standard_name = "lwe_thickness_of_water_evaporation_amount"
ncf2var[:] = e[:]
del ncf2var

fv_msl = get_fill_value(ncf_i, 'msl')
ncf2var = ncf2.createVariable('msl', 'f4', ('time','latitude','longitude'), fill_value=fv_msl)
ncf2var.units = "Pa"
ncf2var.long_name = "Mean sea level pressure"
ncf2var.standard_name = "air_pressure_at_mean_sea_level"
ncf2var[:] = msl[:]
del ncf2var

fv_slhf = get_fill_value(ncf_a, 'slhf')
ncf2var = ncf2.createVariable('slhf', 'f4', ('time','latitude','longitude'), fill_value=fv_slhf)
ncf2var.units = "J m**-2"
ncf2var.long_name = "Surface latent heat flux"
ncf2var.standard_name = "surface_upward_latent_heat_flux"
ncf2var[:] = slhf[:]
del ncf2var

fv_sshf = get_fill_value(ncf_a, 'sshf')
ncf2var = ncf2.createVariable('sshf', 'f4', ('time','latitude','longitude'), fill_value=fv_sshf)
ncf2var.units = "J m**-2"
ncf2var.long_name = "Surface sensible heat flux"
ncf2var.standard_name = "surface_upward_sensible_heat_flux"
ncf2var[:] = sshf[:]
del ncf2var

fv_ssr = get_fill_value(ncf_a, 'ssr')
ncf2var = ncf2.createVariable('ssr', 'f4', ('time','latitude','longitude'), fill_value=fv_ssr)
ncf2var.units = "J m**-2"
ncf2var.long_name = "Surface net short-wave (solar) radiation"
ncf2var.standard_name = "surface_net_downward_shortwave_flux"
ncf2var[:] = ssr[:]
del ncf2var

fv_str = get_fill_value(ncf_a, 'str')
ncf2var = ncf2.createVariable('str', 'f4', ('time','latitude','longitude'), fill_value=fv_str)
ncf2var.units = "J m**-2"
ncf2var.long_name = "Surface net long-wave (thermal) radiation"
ncf2var.standard_name = "surface_net_upward_longwave_flux"
ncf2var[:] = sntr[:]
del ncf2var

fv_strd = get_fill_value(ncf_a, 'strd')
ncf2var = ncf2.createVariable('strd', 'f4', ('time','latitude','longitude'), fill_value=fv_strd)
ncf2var.units = "J m**-2"
ncf2var.long_name = "Surface long-wave (thermal) radiation downwards"
ncf2var[:] = strd[:]
del ncf2var

fv_t2m = get_fill_value(ncf_i, 't2m')
ncf2var = ncf2.createVariable('t2m', 'f4', ('time','latitude','longitude'), fill_value=fv_t2m)
ncf2var.units = "K"
ncf2var.long_name = "2 metre temperature"
ncf2var[:] = t2m[:]
del ncf2var

fv_tcc = get_fill_value(ncf_i, 'tcc')
ncf2var = ncf2.createVariable('tcc', 'f4', ('time','latitude','longitude'), fill_value=fv_tcc)
ncf2var.units = "(0 - 1)"
ncf2var.long_name = "Total cloud cover"
ncf2var.standard_name = "cloud_area_fraction"
ncf2var[:] = tcc[:]
del ncf2var

fv_tp = get_fill_value(ncf_a, 'tp')
ncf2var = ncf2.createVariable('tp', 'f4', ('time','latitude','longitude'), fill_value=fv_tp)
ncf2var.units = "m"
ncf2var.long_name = "Total precipitation"
ncf2var[:] = tp[:]
del ncf2var

# ====================================================
# 关闭文件
# ====================================================
ncf_i.close()
ncf_a.close()
ncf2.close()

print("✅ Conversion complete. Fill values copied from ERA5 source.")
