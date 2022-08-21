import act
import glob
import matplotlib.pyplot as plt
import pandas as pd
import os

files = glob.glob('/Users/atheisen/Code/Pi-Projects/data/sps30/20220*')

names = ['time', 'pc_0_5', 'pc_1_0', 'pc_2_5', 'pc_4_0', 'pc_10_0',
         'mc_1_0', 'mc_2_5', 'mc_4_0', 'mc_10_0','particle_size',
         'particle_size_unit', 'particle_count_unit', 'mass_density_unit']


#df = pd.read_csv(files[0], index_col=0, names=names, parse_dates=True)
#obj = df.to_xarray()
obj = act.io.csvfiles.read_csv(files, column_names=names, parse_dates=True, index_col=0, ignore_index=False)
da = obj['mc_2_5'].rolling(time=10).mean()

obj['mc_2_5'] = da

token = os.getenv('AIRNOW_API')
latlon = '-88.3,41.7,-87.9,41.9'
obj2 = act.discovery.get_airnow.get_airnow_bounded_obs(token, '2022-08-15T00', '2022-08-19T23', latlon, parameters='PM25')
obj2 = obj2.squeeze(dim='sites', drop=False)

print(type(obj2['time'].values[0]))
display = act.plotting.TimeSeriesDisplay({'sps30': obj, 'epa': obj2})
display.plot('mc_2_5', linestyle='None', set_title='PM2.5', dsname='sps30', label='SPS30')
display.plot('PM2.5', linestyle='None', set_title='PM2.5', dsname='epa', label='EPA')
plt.legend()
plt.show()
