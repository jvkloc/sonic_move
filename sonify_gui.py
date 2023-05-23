# Sonify Dear PyGUI dashboard program code
import dearpygui.dearpygui as dpg # https://dearpygui.readthedocs.io/en/latest/
import sonify_functions as sf
from sonify_recorder import start, stop
# create context and viewport
dpg.create_context()
vp = dpg.create_viewport(title='Sonify dashboard')
# get viewport width
vp_width = dpg.get_viewport_width() 
# set dancer window labels and positions
wndw_lbl = ['one', 'two', 'three']
wndw_pos = [(45,200), (25,220), (5,240)]
# set x axis to five seconds (100 Hz = 100 packets per second)
x_axis = list(range(500))
# set sensor status text field width
width = 100
# set height of sensor data plots
height = 350
# create sensor status display window
with dpg.window(label='Recording control panel', pos=(25,0), width=vp_width): 
    # create buttons for recording
    dpg.add_button(label='Start recording', callback=start)
    dpg.add_button(label='Stop recording', callback=stop)    
# create sensor status display window
with dpg.window(label='MTw2 sensor status panel', pos=(25,100), width=vp_width): 
    with dpg.table(header_row=False):
        for i in range(9):
            dpg.add_table_column()
        with dpg.table_row():
            for i in range(9):
                dpg.add_text(f'Waiting for id', tag=f'mtw2{i}')
        with dpg.table_row():
            for i in range(9):
                dpg.add_input_text(tag=f'sensor_{i}', width=width) 
                dpg.set_value(f'sensor_{i}', 'No signal')   
# create window for sensors of each dancer
for w in range(3):
    with dpg.window(label=f'Dancer {wndw_lbl[w]}', pos=wndw_pos[w], width=vp_width, collapsed=True):
        with dpg.table(header_row=False):
            # three columns and two rows for six data types of each sensor
            for _ in range(3):
                dpg.add_table_column()
            for i in range(3):
                # plot tag=data_typedancer_sensorcoordinate
                with dpg.table_row():
                    # create plot for acceleration
                    with dpg.plot(tag=f'dncr{w+1}_mtw2{i+1}_acc', label='Waiting for id...', height=height):
                        # create legend
                        dpg.add_plot_legend()    
                        # create x axis
                        dpg.add_plot_axis(dpg.mvXAxis, label='x')
                        # create y axis for acceleration in x axis direction
                        item = dpg.add_plot_axis(dpg.mvYAxis, label='x acceleration')
                        dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{i+1}']['acc_x'], label='x', tag=f'acc{w}_{i+1}x', parent=dpg.last_item())
                        dpg.set_axis_limits(item, 0, 2)
                        # create y axis for acceleration in y axis direction
                        item = dpg.add_plot_axis(dpg.mvYAxis, label='y acceleration')
                        dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{i+1}']['acc_y'], label='y', tag=f'acc{w}_{i+1}y', parent=dpg.last_item())
                        dpg.set_axis_limits(item, 0, 2)
                        # create y axis for acceleration in z axis direction
                        item = dpg.add_plot_axis(dpg.mvYAxis, label='z acceleration')
                        dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{i+1}']['acc_z'], label='z', tag=f'acc{w}_{i+1}z', parent=dpg.last_item())
                        dpg.set_axis_limits(item, 0, 2)
                    # create plot for velocity
                    with dpg.plot(tag=f'dncr{w+1}_mtw2{i+1}_tot_a', label='Waiting for id...', height=height):
                        # create legend
                        dpg.add_plot_legend()    
                        # create x axis
                        dpg.add_plot_axis(dpg.mvXAxis, label='x')
                        # create y axis for velocity
                        item = dpg.add_plot_axis(dpg.mvYAxis, label='Total Acceleration')
                        dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{i+1}']['tot_a'], label='tot_a', tag=f'tot_a{w}_{i+1}', parent=dpg.last_item())
                        dpg.set_axis_limits(item, 0, 2)
                    # create plot for orientation data
                    with dpg.plot(tag=f'dncr{w+1}_mtw2{i+1}_ori', label='Waiting for id...', height=height):
                        # create legend
                        dpg.add_plot_legend()    
                        # create x axis
                        dpg.add_plot_axis(dpg.mvXAxis, label='x')
                        # create y axis for acceleration in x axis direction
                        item = dpg.add_plot_axis(dpg.mvYAxis, label='x orientation')
                        dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{i+1}']['ori_p'], label='pitch', tag=f'ori{w}_{i+1}p', parent=dpg.last_item())
                        dpg.set_axis_limits(item, 0, 2)
                        # create y axis for acceleration in y axis direction
                        item = dpg.add_plot_axis(dpg.mvYAxis, label='y orientation')
                        dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{i+1}']['ori_r'], label='roll', tag=f'ori{w}_{i+1}r', parent=dpg.last_item())
                        dpg.set_axis_limits(item, 0, 2)
                        # create y axis for acceleration in z axis direction
                        item = dpg.add_plot_axis(dpg.mvYAxis, label='z orientation')
                        dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{i+1}']['ori_y'], label='yaw', tag=f'ori{w}_{i+1}y', parent=dpg.last_item()) 
                        dpg.set_axis_limits(item, 0, 2)
                with dpg.table_row():
                    # create plot for gyroscope data
                    with dpg.plot(tag=f'dncr{w+1}_mtw2{i+1}_gyr', label='Waiting for id...', height=height):
                        # create legend
                        dpg.add_plot_legend()    
                        # create x axis
                        dpg.add_plot_axis(dpg.mvXAxis, label='x')
                        # create y axis for acceleration in x axis direction
                        item = dpg.add_plot_axis(dpg.mvYAxis, label='x gyroscope')
                        dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{i+1}']['gyr_x'], label='x', tag=f'gyr{w}_{i+1}x', parent=dpg.last_item())
                        dpg.set_axis_limits(item, 0, 2)
                        # create y axis for acceleration in y axis direction
                        item = dpg.add_plot_axis(dpg.mvYAxis, label='y gyroscope')
                        dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{i+1}']['gyr_y'], label='y', tag=f'gyr{w}_{i+1}y', parent=dpg.last_item())
                        dpg.set_axis_limits(item, 0, 2)
                        # create y axis for acceleration in z axis direction
                        item = dpg.add_plot_axis(dpg.mvYAxis, label='z gyroscope')
                        dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{i+1}']['gyr_z'], label='z', tag=f'gyr{w}_{i+1}z', parent=dpg.last_item())
                        dpg.set_axis_limits(item, 0, 2)
                    # create plot for rate of turn data
                    with dpg.plot(tag=f'dncr{w+1}_mtw2{i+1}_rot', label='Waiting for id...', height=height):
                        # create legend
                        dpg.add_plot_legend()    
                        # create x axis
                        dpg.add_plot_axis(dpg.mvXAxis, label='x')
                        # create y axis for velocity
                        item = dpg.add_plot_axis(dpg.mvYAxis, label='Rate of Turn')
                        dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{i+1}']['rot'], label='RoT', tag=f'rot{w}_{i+1}', parent=dpg.last_item())
                        dpg.set_axis_limits(item, 0, 2)
                    # create plot for magnetomter data
                    with dpg.plot(tag=f'dncr{w+1}_mtw2{i+1}_mag', label='Waiting for id...', height=height):
                        # create legend
                        dpg.add_plot_legend()    
                        # create x axis
                        dpg.add_plot_axis(dpg.mvXAxis, label='x')
                        # create y axis for acceleration in x axis direction
                        item = dpg.add_plot_axis(dpg.mvYAxis, label='x magnetometer')
                        dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{i+1}']['mag_x'], label='x', tag=f'mag{w}_{i+1}x', parent=dpg.last_item())
                        dpg.set_axis_limits(item, 0, 2)
                        # create y axis for acceleration in y axis direction
                        item = dpg.add_plot_axis(dpg.mvYAxis, label='y magnetometer')
                        dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{i+1}']['mag_z'], label='y', tag=f'mag{w}_{i+1}y', parent=dpg.last_item())
                        dpg.set_axis_limits(item, 0, 2)
                        # create y axis for acceleration in z axis direction
                        item = dpg.add_plot_axis(dpg.mvYAxis, label='z magnetometer')
                        dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{i+1}']['mag_z'], label='z', tag=f'mag{w}_{i+1}z', parent=dpg.last_item())
                        dpg.set_axis_limits(item, 0, 2)
# run the GUI
dpg.setup_dearpygui()
dpg.maximize_viewport()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
