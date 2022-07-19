import pandas as pd
import xarray as xr
import datetime as dt
from as7262 import AS7262

as7262 = AS7262()

as7262.set_illumination_led(False)
as7262.set_gain(3.7)
as7262.set_integration_time(17.857)
as7262.set_measurement_mode(3)

values = as7262.get_calibrated_values()

with open('/home/theisen/spectra3.txt', 'a') as myfile:
    myfile.write(','.join([str(dt.datetime.now()),str(values.red), str(values.orange), str(values.yellow), str(values.green), str(values.blue), str(values.violet), '\n']))
