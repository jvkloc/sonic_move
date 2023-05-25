# functions for sonify_gui.py and sonify_recorder.py
import dearpygui.dearpygui as dpg # https://dearpygui.readthedocs.io/en/latest/
from math import floor
# labels for setting MTw2 ids to dashboard
labels = [ ['acc','Acceleration'], ['tot_a', 'Total Acceleration'], ['ori', 'Orientation'], 
                ['gyr', 'Gyroscope'], ['rot', 'Rate of Turn'], ['mag', 'Magnetometer'] ]
# sensor max and min values for data normalisation, 'key':[x, y, z] or 'key':[p, r, y] for Euler angles
sensors = []
for i in range(9):
    sensors.append({'id': None, 'acc_min':[0, 0, 0], 'gyr_min':[0, 0, 0], 'mag_min':[0, 0, 0], 
                                 'ori_min':[0, 0, 0], 'tot_a_min':[0], 'rot_min':[0],
                                 'acc_max':[1, 1, 1], 'gyr_max':[1, 1, 1], 'mag_max':[1, 1, 1], 
                                 'ori_max':[1, 1, 1], 'tot_a_max':[1], 'rot_max':[1]})
# initialise y-axes data for data plots
dancer_1, dancer_2, dancer_3, snsr_1, snsr_2, snsr_3 = {}, {}, {}, {}, {}, {}
dancers = [dancer_1, dancer_2, dancer_3]
for i in range(3):
    dancers[i]['snsr_1'] = snsr_1
    dancers[i]['snsr_2'] = snsr_2
    dancers[i]['snsr_3'] = snsr_3
# set sensors for each dancer. this needs to be hardcoded, now it's random sensors in the order of initialisation
coord = ['x', 'y', 'z']
for i in range(3):   
    # initialise velocity, rate of turn and euler angles data for each dancer's each sensor
    for j in range(3):
        dancers[i][f'snsr_{j+1}']['tot_a'] = [0]*500
        dancers[i][f'snsr_{j+1}']['bin_tot_a'] = [0]*500
        dancers[i][f'snsr_{j+1}']['rot'] = [0]*500
        dancers[i][f'snsr_{j+1}']['ori_p'] = [0]*500
        dancers[i][f'snsr_{j+1}']['ori_r'] = [0]*500
        dancers[i][f'snsr_{j+1}']['ori_y'] = [0]*500
        # initialise xyz-coordinate data for each dancer
        for data_type in  ['acc', 'gyr' , 'mag']:
            for h in range(len(coord)):
                dancers[i][f'snsr_{j+1}'][f'{data_type}_{coord[h]}'] = [0]*500
# handler function for sending osc4py3 messages
def handler(acc ,vel, gyr, rot, mag, ori, mtw2_id):
    print(acc ,vel, gyr, rot, mag, ori, mtw2_id)                
# function for setting the sensor ids to dashboard and to the normalisation dictionary
def set_sensor_ids(sensor_ids, sensor_locations):
    for i in range(len(sensor_ids)): 
        w = floor(i/3)
        k = i - 3*w + 1
        # set sensor ids to sensors dictionary
        sensors[i]['id'] = sensor_ids[i]
        # set dashboard plot labels
        for j in range(6):
            #dpg.configure_item(f'dncr{w+1}_mtw2{k}_{labels[j][0]}', label=f'MTw2 {sensor_ids[i]} {labels[j][1]}') 
            dpg.configure_item(f'dncr{w+1}_mtw2{k}_{labels[j][0]}', label=f'{sensor_locations[sensor_ids[i]][0]} {labels[j][1]}')
# function for normalising sensor data
def normalise(sensor_id, data_type, value):
    normalised_data = []
    # get the sensor by sensor id
    sensor = list(filter(lambda sensor: sensor['id'] == sensor_id, sensors))[0]
    # set new minimum and maximum if necessary
    for i in range(len(value)):
        minimum = sensor[data_type + '_min'][i]
        maximum = sensor[data_type + '_max'][i]
        if value[i] < minimum:
            sensor[data_type + '_min'][i] = value[i]
        elif value[i] > maximum:
            sensor[data_type + '_max'][i] = value[i]
        # convert normalised numpy.float64 value from Xsens Devide API function to Python's native float for osc4py3 message
        normalised_data.append(float((value[i] - minimum) / (maximum - minimum)))
    return normalised_data
# function for setting and sending sensor data values to dashboard plot
def send_data(sensor_id, mtw2_ids, data_type, value): 
    for i in range(len(mtw2_ids)):
        if  sensor_id == mtw2_ids[i]:
            # dancer one, sensor one, two, three -> dancer two, sensor one, two, three -> dance three, sensor one, two, three
            k = floor(i/3)
            s = i - 3*k + 1
            # set xyz-coordinate data to data plot
            if data_type in ['acc', 'gyr', 'mag']:
                for i in range(len(value)):
                    dancers[k][f'snsr_{s}'][f'{data_type}_{coord[i]}'].append(value[i])
                    while len(dancers[k][f'snsr_{s}'][f'{data_type}_{coord[i]}']) > 500:
                        del dancers[k][f'snsr_{s}'][f'{data_type}_{coord[i]}'][0]
                    dpg.configure_item(f'{data_type}{k}_{s}{coord[i]}', y=dancers[k][f'snsr_{s}'][f'{data_type}_{coord[i]}'])                    
            # set Euler angles data to data plot
            elif data_type == 'ori':
                dancers[k][f'snsr_{s}'][f'{data_type}_p'].append(value[0])  
                dancers[k][f'snsr_{s}'][f'{data_type}_r'].append(value[1])
                dancers[k][f'snsr_{s}'][f'{data_type}_y'].append(value[2])
                for char in ['p', 'y', 'r']:
                    while len(dancers[k][f'snsr_{s}'][f'{data_type}_{char}']) > 500:
                        del dancers[k][f'snsr_{s}'][f'{data_type}_{char}'][0]
                    dpg.configure_item(f'{data_type}{k}_{s}{char}', y=dancers[k][f'snsr_{s}'][f'{data_type}_{char}'])
            # set rate of turn data to data plot
            elif data_type == 'rot':
                dancers[k][f'snsr_{s}'][f'{data_type}'].append(value[0])
                while len(dancers[k][f'snsr_{s}'][f'{data_type}']) > 500:
                    del dancers[k][f'snsr_{s}'][f'{data_type}'][0]                  
                dpg.configure_item(f'{data_type}{k}_{s}', y=dancers[k][f'snsr_{s}'][f'{data_type}'])
            # set total acceleration data to data plot
            elif data_type == 'tot_a':
                dancers[k][f'snsr_{s}'][f'{data_type}'].append(value[0])
                dancers[k][f'snsr_{s}'][f'bin_{data_type}'].append(value[1])
                while len(dancers[k][f'snsr_{s}'][f'{data_type}']) > 500:
                    del dancers[k][f'snsr_{s}'][f'{data_type}'][0]
                dpg.configure_item(f'{data_type}{k}_{s}', y=dancers[k][f'snsr_{s}'][f'{data_type}'])
                while len(dancers[k][f'snsr_{s}'][f'bin_{data_type}']) > 500:
                    del dancers[k][f'snsr_{s}'][f'bin_{data_type}'][0]                 
                dpg.configure_item(f'bin_{data_type}{k}_{s}', y=dancers[k][f'snsr_{s}'][f'bin_{data_type}'])              
# function for checking and setting the measurement status of the sensors
def status(mtw2s, mtw2_locations, ids=False, finished=False):
    for i in range(len(mtw2s)):
        if ids:
            dpg.set_value(f'mtw2{i}', mtw2_locations[f'{mtw2s[i].deviceId()}'][0])
        if finished:
            dpg.set_value(f'sensor_{i}', 'Finished')
        elif not mtw2s[i].isMeasuring():
            dpg.set_value(f'sensor_{i}', 'Error!')
        else:
            dpg.set_value(f'sensor_{i}', 'Measuring')
