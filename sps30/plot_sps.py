import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import glob
import act
myFmt = mdates.DateFormatter('%m/%d-%H')

files = glob.glob('/Users/atheisen/Code/Pi-Projects/data/sps30/2026*')
files.sort()
names = ['time', 'pc_0_5', 'pc_1_0', 'pc_2_5', 'pc_4_0', 'pc_10_0',
         'mc_1_0', 'mc_2_5', 'mc_4_0', 'mc_10_0','particle_size',
         'particle_size_unit', 'particle_count_unit', 'mass_density_unit']

# Open the SP file
ds = act.io.text.read_csv(files, column_names=names, parse_dates=True, index_col=0, ignore_index=False, engine='c')

# Sort the times to be sure there aren't any issues
df = ds.sortby('time')


#df = pd.read_csv(file, index_col=0, names=names, parse_dates=True)
ax = df['mc_2_5'].plot()
#ax.xaxis.set_major_formatter(myFmt)
plt.show()
