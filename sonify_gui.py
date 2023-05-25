# Sonic Move Dear PyGUI dashboard program code
import dearpygui.dearpygui as dpg # https://dearpygui.readthedocs.io/en/latest/
import sonify_functions as sf
from sonify_recorder import start, stop, set_threshold
# create context and viewport
dpg.create_context()
vp = dpg.create_viewport(title='Sonify dashboard')
# get viewport width
vp_width = dpg.get_viewport_width() 
# set dancer window labels and positions
wndw_lbl = ['one', 'two', 'three']
wndw_pos = [(45,300), (25,320), (5,340)]
# set x axis to five seconds (100 Hz = 100 packets per second)
x_axis = list(range(500))
# create program status display window
with dpg.window(label='Recording control panel', pos=(25,0), width=vp_width): 
    # create buttons for recording
    dpg.add_button(label='Start recording', callback=start)
    dpg.add_button(label='Stop recording', callback=stop)
    dpg.add_text('Use mouse to scroll down program message history. First message is in the bottom row.')
    dpg.add_input_text(tag='program_status', width=vp_width, multiline=True)
# create sensor status display window
with dpg.window(label='MTw2 sensor status panel', pos=(25,195), width=vp_width): 
    with dpg.table(header_row=False):
        for i in range(9):
            dpg.add_table_column()
        with dpg.table_row():
            for i in range(9):
                dpg.add_text('Waiting for id', tag=f'mtw2{i}')
        with dpg.table_row():
            for i in range(9):
                dpg.add_text('No signal', tag=f'sensor_{i}')
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
                    # create plot for acceleration data
                    with dpg.plot(tag=f'dncr{w+1}_mtw2{i+1}_acc', label='Waiting for id...'):
                        # create legend
                        dpg.add_plot_legend()    
                        # create x axis
                        dpg.add_plot_axis(dpg.mvXAxis) 
                        # create y axis for acceleration data in x axis direction
                        item = dpg.add_plot_axis(dpg.mvYAxis)
                        dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{i+1}']['acc_x'], label='x', tag=f'acc{w}_{i+1}x', parent=dpg.last_item())
                        dpg.set_axis_limits(item, 0, 1)
                        # create y axis for acceleration data in y axis direction
                        item = dpg.add_plot_axis(dpg.mvYAxis)
                        dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{i+1}']['acc_y'], label='y', tag=f'acc{w}_{i+1}y', parent=dpg.last_item())
                        dpg.set_axis_limits(item, 0, 1)
                        # create y axis for acceleration data in z axis direction
                        item = dpg.add_plot_axis(dpg.mvYAxis)
                        dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{i+1}']['acc_z'], label='z', tag=f'acc{w}_{i+1}z', parent=dpg.last_item())
                        dpg.set_axis_limits(item, 0, 1)
                    # create plot for total acceleration data
                    with dpg.plot(tag=f'dncr{w+1}_mtw2{i+1}_tot_a', label='Waiting for id...'):
                        # create legend
                        dpg.add_plot_legend()    
                        # create x axis
                        dpg.add_plot_axis(dpg.mvXAxis)
                        # create y axis for total acceleration data
                        item = dpg.add_plot_axis(dpg.mvYAxis)
                        dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{i+1}']['tot_a'], label='acc', tag=f'tot_a{w}_{i+1}', parent=dpg.last_item())
                        dpg.set_axis_limits(item, 0, 50)
                        dpg.add_drag_line(default_value=30, vertical=False, label="threshold", color=[255, 0, 0, 255], callback=set_threshold)
                        # create y axis for total acceleration binary data
                        item = dpg.add_plot_axis(dpg.mvYAxis, label='bin')
                        dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{i+1}']['bin_tot_a'], label='0/1', tag=f'bin_tot_a{w}_{i+1}', parent=dpg.last_item())
                        dpg.set_axis_limits(item, 0, 1)                        
                    # create plot for orientation data
                    with dpg.plot(tag=f'dncr{w+1}_mtw2{i+1}_ori', label='Waiting for id...'):
                        # create legend
                        dpg.add_plot_legend()    
                        # create x axis
                        dpg.add_plot_axis(dpg.mvXAxis)
                        # create y axis for orientation data in x axis direction
                        item = dpg.add_plot_axis(dpg.mvYAxis)
                        dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{i+1}']['ori_p'], label='pitch', tag=f'ori{w}_{i+1}p', parent=dpg.last_item())
                        dpg.set_axis_limits(item, 0, 1)
                        # create y axis for orientation data in y axis direction
                        item = dpg.add_plot_axis(dpg.mvYAxis)
                        dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{i+1}']['ori_r'], label='roll', tag=f'ori{w}_{i+1}r', parent=dpg.last_item())
                        dpg.set_axis_limits(item, 0, 1)
                        # create y axis for orientation data in z axis direction
                        item = dpg.add_plot_axis(dpg.mvYAxis)
                        dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{i+1}']['ori_y'], label='yaw', tag=f'ori{w}_{i+1}y', parent=dpg.last_item()) 
                        dpg.set_axis_limits(item, 0, 1)
                with dpg.table_row():
                    # create plot for gyroscope data
                    with dpg.plot(tag=f'dncr{w+1}_mtw2{i+1}_gyr', label='Waiting for id...'):
                        # create legend
                        dpg.add_plot_legend()    
                        # create x axis
                        dpg.add_plot_axis(dpg.mvXAxis)
                        # create y axis for gyroscope data in x axis direction
                        item = dpg.add_plot_axis(dpg.mvYAxis)
                        dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{i+1}']['gyr_x'], label='x', tag=f'gyr{w}_{i+1}x', parent=dpg.last_item())
                        dpg.set_axis_limits(item, 0, 1)
                        # create y axis for gyroscope data in y axis direction
                        item = dpg.add_plot_axis(dpg.mvYAxis)
                        dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{i+1}']['gyr_y'], label='y', tag=f'gyr{w}_{i+1}y', parent=dpg.last_item())
                        dpg.set_axis_limits(item, 0, 1)
                        # create y axis for gyroscope data in z axis direction
                        item = dpg.add_plot_axis(dpg.mvYAxis)
                        dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{i+1}']['gyr_z'], label='z', tag=f'gyr{w}_{i+1}z', parent=dpg.last_item())
                        dpg.set_axis_limits(item, 0, 1)
                    # create plot for rate of turn data
                    with dpg.plot(tag=f'dncr{w+1}_mtw2{i+1}_rot', label='Waiting for id...'):
                        # create legend
                        dpg.add_plot_legend()    
                        # create x axis
                        dpg.add_plot_axis(dpg.mvXAxis)
                        # create y axis for rate of turn data
                        item = dpg.add_plot_axis(dpg.mvYAxis)
                        dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{i+1}']['rot'], label='rot', tag=f'rot{w}_{i+1}', parent=dpg.last_item())
                        dpg.set_axis_limits(item, 0, 1)
                    # create plot for magnetomter data
                    with dpg.plot(tag=f'dncr{w+1}_mtw2{i+1}_mag', label='Waiting for id...'):
                        # create legend
                        dpg.add_plot_legend()    
                        # create x axis
                        dpg.add_plot_axis(dpg.mvXAxis)
                        # create y axis for magnetomter data in x axis direction
                        item = dpg.add_plot_axis(dpg.mvYAxis)
                        dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{i+1}']['mag_x'], label='x', tag=f'mag{w}_{i+1}x', parent=dpg.last_item())
                        dpg.set_axis_limits(item, 0, 1)
                        # create y axis for magnetomter data in y axis direction
                        item = dpg.add_plot_axis(dpg.mvYAxis)
                        dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{i+1}']['mag_z'], label='y', tag=f'mag{w}_{i+1}y', parent=dpg.last_item())
                        dpg.set_axis_limits(item, 0, 1)
                        # create y axis for magnetomter data in z axis direction
                        item = dpg.add_plot_axis(dpg.mvYAxis)
                        dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{i+1}']['mag_z'], label='z', tag=f'mag{w}_{i+1}z', parent=dpg.last_item())
                        dpg.set_axis_limits(item, 0, 1)
# run the GUI
dpg.setup_dearpygui()
dpg.maximize_viewport()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
