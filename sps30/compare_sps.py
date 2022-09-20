import act
import glob
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np

files = glob.glob('/Users/atheisen/Code/Pi-Projects/data/sps30/20220919*')
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
obj2 = act.discovery.get_airnow.get_airnow_bounded_obs(token, '2022-09-19T00', '2022-09-19T23', latlon, parameters='PM25')

print(obj2['PM2.5'].values)
display = act.plotting.TimeSeriesDisplay({'sps30': obj, 'epa': obj2})
display.plot('mc_2_5', set_title='PM2.5', dsname='sps30', label='SPS30 2.5')
display.plot('PM2.5', set_title='PM2.5', dsname='epa', label=['Cary','Naperville'], force_line_plot=True)
display.day_night_background('sps30')
plt.legend()
plt.show()
