# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 10:56:23 2024

@author: X.Zhou @SKLEC (Sh. CN) & NIVA (BG. Nor)
"""
import cdsapi

c = cdsapi.Client()
dataset = "reanalysis-era5-single-levels"
request = {
    "product_type": ["reanalysis"],
    "variable": [
        "10m_u_component_of_wind",
        "10m_v_component_of_wind",
        "mean_sea_level_pressure",
        "2m_dewpoint_temperature",
        "2m_temperature",
        "total_precipitation",
        "surface_latent_heat_flux",
        "surface_net_solar_radiation",
        "surface_net_thermal_radiation",
        "surface_sensible_heat_flux",
        "surface_thermal_radiation_downwards",
        "total_cloud_cover",
        "evaporation"
    ],
    "year": ["2022", "2023"],
    "month": [
        "01", "02", "03",
        "04", "05", "06",
        "07", "08", "09",
        "10", "11", "12"
    ],
    "day": [
        "01", "02", "03",
        "04", "05", "06",
        "07", "08", "09",
        "10", "11", "12",
        "13", "14", "15",
        "16", "17", "18",
        "19", "20", "21",
        "22", "23", "24",
        "25", "26", "27",
        "28", "29", "30",
        "31"
    ],
    "time": [
        "00:00", "03:00", "06:00",
        "09:00", "12:00", "15:00",
        "18:00", "21:00"
    ],
    "data_format": "netcdf",
    "download_format": "unarchived",
    "area": [45, 105, 10, 134]
}

client = cdsapi.Client()
client.retrieve(dataset, request).download(r'D:\public\newERA.zip')

