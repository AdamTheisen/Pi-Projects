import os
import glob
from datetime import datetime
import numpy as np
import pandas as pd

import act
import matplotlib.pyplot as plt
import xarray as xr

files = glob.glob('/Users/atheisen/Code/Pi-Projects/data/sps30/2026*')
files.sort()

# Extract dates from filenames
start = datetime.strptime(os.path.basename(files[0]).split('.')[0], "%Y%m%d")
end = datetime.strptime(os.path.basename(files[-1]).split('.')[0], "%Y%m%d")

# Format for AirNow API
start_date = start.strftime("%Y-%m-%dT00")
end_date = end.strftime("%Y-%m-%dT23")

names = ['time', 'pc_0_5', 'pc_1_0', 'pc_2_5', 'pc_4_0', 'pc_10_0',
         'mc_1_0', 'mc_2_5', 'mc_4_0', 'mc_10_0','particle_size',
         'particle_size_unit', 'particle_count_unit', 'mass_density_unit']

# Open the SP file
obj = act.io.text.read_csv(files, column_names=names, parse_dates=True, index_col=0, ignore_index=False, engine='c')

# Remove invalid timestamps
obj = obj.isel(time=~pd.isna(obj.time.values))

# Sort timestamps
obj = obj.sortby('time')

# Remove duplicate timestamps
_, idx = np.unique(obj.time.values, return_index=True)
obj = obj.isel(time=np.sort(idx))

# Remove negative PM measurements
for var in ['mc_1_0', 'mc_2_5', 'mc_4_0', 'mc_10_0']:
    obj[var] = obj[var].where(obj[var] >= 0)

# Average to 1 hour
obj = obj.resample(time='1h').mean()

#display = act.plotting.TimeSeriesDisplay(obj)
#display.plot('mc_2_5', label='SPS30 PM2.5')
#plt.show()

# Set Lat/lon of the system
obj['lat'] = 45.023
obj['lon'] = -92.8602

# Needs an AIRNOW_API environment variable set with your TOKEN
# sign up here: https://docs.airnowapi.org/
token = os.getenv('AIRNOW_API')

# Set Lat/lon box for EPA sites
latlon = '-93.2,44.79,-92.68,45.12'

# Get EPA data
obj2 = act.discovery.airnow.get_airnow_bounded_obs(token, start_date, end_date, latlon, parameters='PM25')
obj2['PM2.5'] = obj2['PM2.5'].where(obj2['PM2.5'] >= 0)

sites = obj2['sites'].values
display = act.plotting.TimeSeriesDisplay({'sps30': obj, 'epa': obj2})
display.plot('mc_1_0', dsname='sps30', label='SPS30 PM1')
display.plot('mc_2_5', dsname='sps30', label='SPS30 PM2.5')
display.plot('mc_10_0', dsname='sps30', label='SPS30 PM10')
display.plot('PM2.5', set_title='PM2.5', dsname='epa', label=[sites], force_line_plot=True)
display.day_night_background('sps30')
plt.legend()
plt.show()

print(obj2)

ds = xr.merge([obj, obj2])

# Extract valid data
x = ds['mc_2_5'].values
y = ds['PM2.5'].isel(sites=0).values

# Remove NaNs
mask = np.isfinite(x) & np.isfinite(y)
x = x[mask]
y = y[mask]

# Fit linear trend
m, b = np.polyfit(x, y, 1)

# Plot trend line
xfit = np.linspace(x.min(), x.max(), 100)

display = act.plotting.DistributionDisplay(ds, figsize=(12,10))
title = 'St. Paul-Harding H.S. EPA Station PM2.5 vs SPS30 PM'
display.plot_scatter('mc_2_5', 'PM2.5', set_title=title)
display.axes[0].plot([0,100], [0, 100])

display.axes[0].plot(
    xfit,
    m * xfit + b,
    color='red',
    linewidth=2,
    label=f'Fit: y={m:.2f}x + {b:.2f}'
)

r = np.corrcoef(x, y)[0, 1]
r2 = r**2

display.axes[0].text(
    0.05, 0.95,
    f'$R^2$ = {r2:.3f}\nSlope = {m:.2f}\nOffset = {b:.2f}',
    transform=display.axes[0].transAxes,
    va='top',
    bbox=dict(facecolor='white', alpha=0.8)
)

display.set_yrng([0, 100])
display.set_xrng([0, 100])
plt.show()
#ds['car_pm2.5'] = xr.DataArray(data=ds['PM2.5'].values[:, 0], dims=['time'], coords={'time': ds['time'].values})
#ds['nap_pm2.5'] = xr.DataArray(data=ds['PM2.5'].values[:, 1], dims=['time'], coords={'time': ds['time'].values})
#display = act.plotting.DistributionDisplay(ds, subplot_shape=(2, 2), figsize=(12,10))

#title = 'Cary EPA Station PM2.5 vs SPS30 PM'
#display.plot_scatter('mc_2_5', 'car_pm2.5', subplot_index=(0, 0), set_title=title)
#title = 'Naperville EPA Station PM2.5 vs SPS30 PM'
#display.plot_scatter('mc_2_5', 'nap_pm2.5', subplot_index=(0, 1), set_title=title)
#title = 'Cary EPA Station PM2.5 vs SPS30 PM2.5'
#display.plot_heatmap('mc_2_5', 'car_pm2.5', subplot_index=(1, 0), threshold=0, x_bins=50, y_bins=50, set_title=title)
#title = 'Naperville EPA Station PM2.5 vs SPS30 PM2.5'
#display.plot_heatmap('mc_2_5', 'nap_pm2.5', subplot_index=(1, 1), threshold=0, x_bins=50, y_bins=50, set_title=title)
#limits = [0, 205]
#for ax in display.axes:
#    ax[0].set_xlim(limits)
#    ax[0].set_ylim(limits)
#    ax[1].set_xlim(limits)
#    ax[1].set_ylim(limits)
