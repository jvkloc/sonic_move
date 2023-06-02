# Sonic Move Dear PyGUI dashboard program code for displaying four sensors in a row
import dearpygui.dearpygui as dpg # https://dearpygui.readthedocs.io/en/latest/
import sm_functions as sf
from sonic_move_main import start, stop, set_threshold
# create context and viewport
dpg.create_context()
vp = dpg.create_viewport(title='Sonify dashboard')
# get viewport width
vp_width = dpg.get_viewport_width() + 215
# set dancer window labels and positions
wndw_lbl = ['one', 'two', 'three']
wndw_pos = [(45,300), (25,320), (5,340)]
# set x axis to five seconds (100 Hz = 100 packets per second)
x_axis = list(range(500))
# create program status display window
with dpg.window(label='Recording control panel', pos=(25,0), width=vp_width-215): 
    # create buttons for recording
    dpg.add_button(label='Start recording', callback=start)
    dpg.add_button(label='Stop recording', callback=stop)    
    dpg.add_input_text(tag='program_status', width=vp_width, multiline=True)
# create sensor status display window
with dpg.window(label='MTw2 sensor status panel', pos=(25,195), width=vp_width-215): 
    with dpg.table(header_row=False):
        for i in range(9):
            dpg.add_table_column()
        with dpg.table_row():
            for i in range(9):
                dpg.add_text('Waiting for id', tag=f'mtw2{i}')
        with dpg.table_row():
            for i in range(9):
                dpg.add_text( 'No signal', tag=f'sensor_{i}') 
    dpg.add_text('Click on plot legend variables to show or hide related data')
# create window for sensors of each dancer
for w in range(3):
    with dpg.window(label=f'Dancer {wndw_lbl[w]}', pos=wndw_pos[w], width=vp_width, collapsed=True):
        with dpg.table(header_row=False):
            # four columns 
            for _ in range(4):
                dpg.add_table_column()
            #for i in range(3):
            # plot tag=data_typedancer_sensorcoordinate
            with dpg.table_row():
                # create plot for acceleration data, sensor 1
                with dpg.plot(tag=f'dncr{w+1}_mtw2{1}_acc', label='Waiting for id...'):
                    # create legend
                    dpg.add_plot_legend()    
                    # create x axis
                    dpg.add_plot_axis(dpg.mvXAxis)
                    # create y axis for acceleration data in x axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{1}']['acc_x'], label='x', tag=f'acc{w}_{1}x', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
                    # create y axis for acceleration data in y axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{1}']['acc_y'], label='y', tag=f'acc{w}_{1}y', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
                    # create y axis for acceleration data in z axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{1}']['acc_z'], label='z', tag=f'acc{w}_{1}z', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
                # create plot for total acceleration data, sensor 1
                with dpg.plot(tag=f'dncr{w+1}_mtw2{1}_tot_a', label='Waiting for id...'):
                    # create legend
                    dpg.add_plot_legend()    
                    # create x axis
                    dpg.add_plot_axis(dpg.mvXAxis)
                    # create y axis for total acceleration data
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{1}']['tot_a'], label='acc', tag=f'tot_a{w}_{1}', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 50)
                    dpg.add_drag_line(default_value=30, vertical=False, label="threshold", color=[255, 0, 0, 255], callback=set_threshold)
                    # create y axis for total acceleration binary data
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{1}']['bin_tot_a'], label='0/1', tag=f'bin_tot_a{w}_{1}', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)                 
                # create plot for orientation data, sensor 1
                with dpg.plot(tag=f'dncr{w+1}_mtw2{1}_ori', label='Waiting for id...'):
                    # create legend
                    dpg.add_plot_legend()    
                    # create x axis
                    dpg.add_plot_axis(dpg.mvXAxis)
                    # create y axis for orientation data in x axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{1}']['ori_p'], label='pitch', tag=f'ori{w}_{1}p', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
                    # create y axis for orientation data in y axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{1}']['ori_r'], label='roll', tag=f'ori{w}_{1}r', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
                    # create y axis for orientation data in z axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{1}']['ori_y'], label='yaw', tag=f'ori{w}_{1}y', parent=dpg.last_item()) 
                    dpg.set_axis_limits(item, 0, 1)
                # create plot for gyroscope data, sensor 1
                with dpg.plot(tag=f'dncr{w+1}_mtw2{1}_gyr', label='Waiting for id...'):
                    # create legend
                    dpg.add_plot_legend()    
                    # create x axis
                    dpg.add_plot_axis(dpg.mvXAxis)
                    # create y axis for gyroscope data in x axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{1}']['gyr_x'], label='x', tag=f'gyr{w}_{1}x', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
                    # create y axis for gyroscope data in y axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{1}']['gyr_y'], label='y', tag=f'gyr{w}_{1}y', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
                    # create y axis for gyroscope data in z axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{1}']['gyr_z'], label='z', tag=f'gyr{w}_{1}z', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
            with dpg.table_row():
                # create plot for rate of turn data, sensor 1
                with dpg.plot(tag=f'dncr{w+1}_mtw2{1}_rot', label='Waiting for id...'):
                    # create legend
                    dpg.add_plot_legend()    
                    # create x axis
                    dpg.add_plot_axis(dpg.mvXAxis)
                    # create y axis for rate of turn data
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{1}']['rot'], label='rot', tag=f'rot{w}_{1}', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
                # create plot for magnetomter data, sensor 1
                with dpg.plot(tag=f'dncr{w+1}_mtw2{1}_mag', label='Waiting for id...'):
                    # create legend
                    dpg.add_plot_legend()    
                    # create x axis
                    dpg.add_plot_axis(dpg.mvXAxis)
                    # create y axis for magnetomter data in x axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{1}']['mag_x'], label='x', tag=f'mag{w}_{1}x', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
                    # create y axis for magnetomter data in y axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{1}']['mag_z'], label='y', tag=f'mag{w}_{1}y', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
                    # create y axis for magnetomter data in z axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{1}']['mag_z'], label='z', tag=f'mag{w}_{1}z', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
                # create plot for acceleration data, sensor 2
                with dpg.plot(tag=f'dncr{w+1}_mtw2{2}_acc', label='Waiting for id...'):
                    # create legend
                    dpg.add_plot_legend()    
                    # create x axis
                    dpg.add_plot_axis(dpg.mvXAxis)
                    # create y axis for acceleration data in x axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{2}']['acc_x'], label='x', tag=f'acc{w}_{2}x', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
                    # create y axis for acceleration data in y axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{2}']['acc_y'], label='y', tag=f'acc{w}_{2}y', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
                    # create y axis for acceleration data in z axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{2}']['acc_z'], label='z', tag=f'acc{w}_{2}z', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
                # create plot for total acceleration data, sensor 2
                with dpg.plot(tag=f'dncr{w+1}_mtw2{2}_tot_a', label='Waiting for id...'):
                    # create legend
                    dpg.add_plot_legend()    
                    # create x axis
                    dpg.add_plot_axis(dpg.mvXAxis)
                    # create y axis for total acceleration data
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{2}']['tot_a'], label='acc', tag=f'tot_a{w}_{2}', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 50)
                    dpg.add_drag_line(default_value=30, vertical=False, label="threshold", color=[255, 0, 0, 255], callback=set_threshold)                    
                    # create y axis for total acceleration binary data
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{2}']['bin_tot_a'], label='0/1', tag=f'bin_tot_a{w}_{2}', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)             
            with dpg.table_row():
                # create plot for orientation data, sensor 2
                with dpg.plot(tag=f'dncr{w+1}_mtw2{2}_ori', label='Waiting for id...'):
                    # create legend
                    dpg.add_plot_legend()    
                    # create x axis
                    dpg.add_plot_axis(dpg.mvXAxis)
                    # create y axis for orientation data in x axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{2}']['ori_p'], label='pitch', tag=f'ori{w}_{2}p', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
                    # create y axis for orientation data in y axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{2}']['ori_r'], label='roll', tag=f'ori{w}_{2}r', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
                    # create y axis for orientation data in z axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{2}']['ori_y'], label='yaw', tag=f'ori{w}_{2}y', parent=dpg.last_item()) 
                    dpg.set_axis_limits(item, 0, 1)
                # create plot for gyroscope data, sensor 2
                with dpg.plot(tag=f'dncr{w+1}_mtw2{2}_gyr', label='Waiting for id...'):
                    # create legend
                    dpg.add_plot_legend()    
                    # create x axis
                    dpg.add_plot_axis(dpg.mvXAxis)
                    # create y axis for gyroscope data in x axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{2}']['gyr_x'], label='x', tag=f'gyr{w}_{2}x', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
                    # create y axis for gyroscope data in y axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{2}']['gyr_y'], label='y', tag=f'gyr{w}_{2}y', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
                    # create y axis for gyroscope data in z axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{2}']['gyr_z'], label='z', tag=f'gyr{w}_{2}z', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)    
                # create plot for rate of turn data, sensor 2
                with dpg.plot(tag=f'dncr{w+1}_mtw2{2}_rot', label='Waiting for id...'):
                    # create legend
                    dpg.add_plot_legend()    
                    # create x axis
                    dpg.add_plot_axis(dpg.mvXAxis,)
                    # create y axis for  rate of turn data
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{2}']['rot'], label='rot', tag=f'rot{w}_{2}', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
                # create plot for magnetomter data, sensor 2
                with dpg.plot(tag=f'dncr{w+1}_mtw2{2}_mag', label='Waiting for id...'):
                    # create legend
                    dpg.add_plot_legend()    
                    # create x axis
                    dpg.add_plot_axis(dpg.mvXAxis)
                    # create y axis for magnetomter data in x axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{2}']['mag_x'], label='x', tag=f'mag{w}_{2}x', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
                    # create y axis for magnetomter data in y axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{2}']['mag_z'], label='y', tag=f'mag{w}_{2}y', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
                    # create y axis for magnetomter data in z axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{2}']['mag_z'], label='z', tag=f'mag{w}_{2}z', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)  
            with dpg.table_row():
                # create plot for acceleration data, sensor 3
                with dpg.plot(tag=f'dncr{w+1}_mtw2{3}_acc', label='Waiting for id...'):
                    # create legend
                    dpg.add_plot_legend()    
                    # create x axis
                    dpg.add_plot_axis(dpg.mvXAxis)
                    # create y axis for acceleration data in x axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{3}']['acc_x'], label='x', tag=f'acc{w}_{3}x', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
                    # create y axis for acceleration data in y axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{3}']['acc_y'], label='y', tag=f'acc{w}_{3}y', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
                    # create y axis for acceleration data in z axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{3}']['acc_z'], label='z', tag=f'acc{w}_{3}z', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
                # create plot for total acceleration data, sensor 3
                with dpg.plot(tag=f'dncr{w+1}_mtw2{3}_tot_a', label='Waiting for id...'):
                    # create legend
                    dpg.add_plot_legend()    
                    # create x axis
                    dpg.add_plot_axis(dpg.mvXAxis)
                    # create y axis for total acceleration data
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{3}']['tot_a'], label='acc', tag=f'tot_a{w}_{3}', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 50)
                    dpg.add_drag_line(default_value=30, vertical=False, label="threshold", color=[255, 0, 0, 255], callback=set_threshold)
                    # create y axis for total acceleration binary data
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{3}']['bin_tot_a'], label='0/1', tag=f'bin_tot_a{w}_{3}', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)                 
                # create plot for orientation data, sensor 3
                with dpg.plot(tag=f'dncr{w+1}_mtw2{3}_ori', label='Waiting for id...'):
                    # create legend
                    dpg.add_plot_legend()    
                    # create x axis
                    dpg.add_plot_axis(dpg.mvXAxis)
                    # create y axis for orientation data in x axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{3}']['ori_p'], label='pitch', tag=f'ori{w}_{3}p', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
                    # create y axis for orientation data in y axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{3}']['ori_r'], label='roll', tag=f'ori{w}_{3}r', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
                    # create y axis for orientation data in z axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{3}']['ori_y'], label='yaw', tag=f'ori{w}_{3}y', parent=dpg.last_item()) 
                    dpg.set_axis_limits(item, 0, 1)
                # create plot for gyroscope data, sensor 3
                with dpg.plot(tag=f'dncr{w+1}_mtw2{3}_gyr', label='Waiting for id...'):
                    # create legend
                    dpg.add_plot_legend()    
                    # create x axis
                    dpg.add_plot_axis(dpg.mvXAxis)
                    # create y axis for gyroscope data in x axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{3}']['gyr_x'], label='x', tag=f'gyr{w}_{3}x', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
                    # create y axis for gyroscope data in y axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{3}']['gyr_y'], label='y', tag=f'gyr{w}_{3}y', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
                    # create y axis for gyroscope data in z axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{3}']['gyr_z'], label='z', tag=f'gyr{w}_{3}z', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
            with dpg.table_row():
                # create plot for rate of turn data, sensor 3
                with dpg.plot(tag=f'dncr{w+1}_mtw2{3}_rot', label='Waiting for id...'):
                    # create legend
                    dpg.add_plot_legend()    
                    # create x axis
                    dpg.add_plot_axis(dpg.mvXAxis)
                    # create y axis for rate of turn data
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{3}']['rot'], label='rot', tag=f'rot{w}_{3}', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
                # create plot for magnetomter data, sensor 1
                with dpg.plot(tag=f'dncr{w+1}_mtw2{3}_mag', label='Waiting for id...'):
                    # create legend
                    dpg.add_plot_legend()    
                    # create x axis
                    dpg.add_plot_axis(dpg.mvXAxis)
                    # create y axis for magnetomter data in x axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{3}']['mag_x'], label='x', tag=f'mag{w}_{3}x', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
                    # create y axis for magnetomter data in y axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{3}']['mag_z'], label='y', tag=f'mag{w}_{3}y', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
                    # create y axis for magnetomter data in z axis direction
                    item = dpg.add_plot_axis(dpg.mvYAxis)
                    dpg.add_line_series(x_axis, sf.dancers[w][f'snsr_{3}']['mag_z'], label='z', tag=f'mag{w}_{3}z', parent=dpg.last_item())
                    dpg.set_axis_limits(item, 0, 1)
# run the GUI
dpg.setup_dearpygui()
dpg.maximize_viewport()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
