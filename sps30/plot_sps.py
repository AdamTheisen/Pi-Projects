import pandas as pd
import matplotlib.pyplot as plt

file = '/home/theisen/data/sps30/test.txt'

names = ['time', 'pc_0_5', 'pc_1_0', 'pc_2_5', 'pc_4_0', 'pc_10_0',
         'md_1_0', 'md_2_5', 'md_4_0', 'md_10_0','particle_size',
         'particle_size_unit', 'particle_count_unit', 'mass_density_unit']
df = pd.read_csv(file, index_col=0, names=names)
df['pc_2_5'].plot()
plt.show()
