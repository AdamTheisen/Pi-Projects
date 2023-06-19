import act
import glob
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
import xarray as xr

files = glob.glob('/Users/atheisen/Code/Pi-Projects/data/sps30/2023061*')
files.sort()
names = ['time', 'pc_0_5', 'pc_1_0', 'pc_2_5', 'pc_4_0', 'pc_10_0',
         'mc_1_0', 'mc_2_5', 'mc_4_0', 'mc_10_0','particle_size',
         'particle_size_unit', 'particle_count_unit', 'mass_density_unit']

# Open the SP file
obj = act.io.csvfiles.read_csv(files, column_names=names, parse_dates=True, index_col=0, ignore_index=False, engine='c')

# Sort the times to be sure there aren't any issues
obj = obj.sortby('time')

# Average to 1 hour
obj = obj.resample(time='1H').mean()

# Set Lat/lon of the system
obj['lat'] = 41.96252
obj['lon'] = -88.12377

# Needs an AIRNOW_API environment variable set with your TOKEN
# sign up here: https://docs.airnowapi.org/
token = os.getenv('AIRNOW_API')

# Set Lat/lon box for EPA sites
latlon = '-88.3,41.7,-87.9,42.3'

# Get EPA data
obj2 = act.discovery.get_airnow.get_airnow_bounded_obs(token, '2023-06-10T00', '2023-06-19T23', latlon, parameters='PM25')

display = act.plotting.TimeSeriesDisplay({'sps30': obj, 'epa': obj2})
display.plot('mc_1_0', dsname='sps30', label='SPS30 PM1')
display.plot('mc_2_5', dsname='sps30', label='SPS30 PM2.5')
display.plot('mc_10_0', dsname='sps30', label='SPS30 PM10')
display.plot('PM2.5', set_title='PM2.5', dsname='epa', label=['Cary','Naperville'], force_line_plot=True)
display.day_night_background('sps30')
plt.legend()
plt.show()

ds = xr.merge([obj, obj2])
ds['car_pm2.5'] = xr.DataArray(data=ds['PM2.5'].values[:, 0], dims=['time'], coords={'time': ds['time'].values})
ds['nap_pm2.5'] = xr.DataArray(data=ds['PM2.5'].values[:, 1], dims=['time'], coords={'time': ds['time'].values})
display = act.plotting.DistributionDisplay(ds, subplot_shape=(1, 2), figsize=(12,5))
display.scatter('mc_2_5', 'car_pm2.5', subplot_index=(0, 0))
display.scatter('mc_2_5', 'nap_pm2.5', subplot_index=(0, 1))
limits = [0,100]
display.axes[0, 0].set_xlim(limits)
display.axes[0, 1].set_xlim(limits)
display.axes[0, 0].set_ylim(limits)
display.axes[0, 1].set_ylim(limits)
plt.show()
