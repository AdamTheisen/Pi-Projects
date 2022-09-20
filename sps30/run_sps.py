import sys
import json
from time import sleep
from sps30 import SPS30
import pandas as pd
import datetime as dt


if __name__ == "__main__":
    pm_sensor = SPS30()
    firmware = pm_sensor.firmware_version()
    sn = pm_sensor.serial_number()
    status = pm_sensor.read_status_register()
    clean_interval = pm_sensor.read_auto_cleaning_interval()
    pm_sensor.start_measurement()

    today = dt.datetime.utcnow().strftime('%Y%m%d')
    f = open('/home/theisen/Code/Pi-Projects/data/sps30/' + today + '.txt', 'a')
    print('Opening file')
    ct = 0
    time = dt.datetime.utcnow()
    while ct < 5:
        #try:
            data = pm_sensor.get_measurement()
            sleep(2)
            if len(data) > 0:
                wdata = []
                multi_vars = ['particle_count', 'mass_density']
                for k in multi_vars:
                    for k2 in data['sensor_data'][k].keys():
                        wdata.append(str(data['sensor_data'][k][k2]))
                wdata.append(str(data['sensor_data']['particle_size']))
                wdata.append(str(data['sensor_data']['particle_size_unit']))
                wdata.append(str(data['sensor_data']['particle_count_unit']))
                wdata.append(str(data['sensor_data']['mass_density_unit']))
                f.write(','.join([str(time)] + wdata)+'\n')

                ct = 5
        #except:
        #    print('error')
        #    pass
            ct += 1
    f.close()

    pm_sensor.stop_measurement()
