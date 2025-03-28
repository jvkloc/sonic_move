"""
Jonne Klockars 2023
HUMEA Lab

Class for Sonic Move Biodata Sonata dashboard.
"""

import sys
import threading

# https://dearpygui.readthedocs.io/en/latest/
import dearpygui.dearpygui as dpg

from sensors import dancers, plot_log
import xda_device as xd


class Dashboard:

    def __init__(self, device, path):
        """
        Parameters
        ----------
        device : str
            'dongle' or 'station' Xsens main device. Default is 'station'.
        path : str
            File path for saving log files. Recommendation is to create a 
            folder just for the logs. 
        Attributes
        ----------
        main_device : XdaDevice
            The main Xsens device used for recording.
        """
        
        self.setup()
        self.main_device = xd.XdaDevice(device, path)

    def set_threshold(self, sender, app_data):
        """Sets a threshold for acceleration."""
        self.main_device.acc_threshold = dpg.get_value(sender)

    def show_file_dialog(self, sender, app_data):
        """Shows log file selection window."""
        dpg.show_item('file_dialog')

    def file_dialog_callback(self, sender, app_data):
        """Callback for plotting a log file."""
        
        log_file_path = app_data['file_path_name']
        data_dicts = dancers()
        axes = ['x', 'y', 'z']
        plot_log(log_file_path, data_dicts, axes)
    
    def recording_switch(self, sender, app_data):
        """Callback for switching recording on and off."""
        
        self.main_device.recording = not self.main_device.recording
        if self.main_device.recording:
            self.main_device.create_control_object()
            self.main_device.open_device()
            self.main_device.configure_device()
            self.main_device.go_to_recording_mode()        
            recording_loop_thread = threading.Thread(
                    target=self.main_device.recording_loop, daemon=True
            )
            recording_loop_thread.start()  
    
    def exit_program(self, sender, app_data):
        """Callback for exitng the program."""
        
        dpg.set_value(
            'program_status', 'Program exited by user.\n\n'
            f'{dpg.get_value("program_status")}'
        )
        print('Program exited by user.')
        try:
            self.main_device.device.disableRadio()
        except Exception as e:
            dpg.set_value(
                'program_status', 'Radio disabling failed.' 
                ' Perhaps it was not on.'
                f'{dpg.get_value("program_status")}'
            )
            print('Radio disabling failed. Perhaps it was not on.')            
        sys.exit(0)        

    def setup(self):
        """Creates a Dear PyGui dashboard. """
        
        initial_data = [0] * 500
        dpg.create_context()
        vp = dpg.create_viewport(title='Sonify dashboard')
        vp_width = dpg.get_viewport_width()
        window_lbl = ['one', 'two', 'three']
        window_pos = [(45,300), (25,320), (5,340)]
        x_axis = list(range(500))
        # Program status display window.
        with dpg.window(label='Recording panel', pos=(25,0), width=vp_width):
            dpg.add_button(
                label='Recording on/off', callback=self.recording_switch
            )            
            dpg.add_button(
                label='Plot txt log file', callback=self.show_file_dialog
            )
            dpg.add_button(label='Quit', callback=self.exit_program)
            dpg.add_text(
                'Use mouse to scroll down program message history. First'
                ' message is in the bottom row.'
            )
            dpg.add_input_text(
                tag='program_status', width=vp_width, multiline=True
            )
        # Sensor status display window.
        with dpg.window(
            label='Sensor status panel', pos=(25,195), width=vp_width
        ):
            with dpg.table(header_row=False):
                for i in range(9):
                    dpg.add_table_column()
                with dpg.table_row():
                    for i in range(9):
                        dpg.add_text('Waiting for id', tag=f'snsr_id{i}')
                with dpg.table_row():
                    for i in range(9):
                        dpg.add_text('No signal', tag=f'sensor_{i}')
            dpg.add_text(
                'Click on plot legend variables to show or hide related data'
            )
        # A window for sensors of each dancer.
        for i in range(3):
            with dpg.window(
                    label=f'Dancer {window_lbl[i]}', pos=window_pos[i],
                    width=vp_width, collapsed=True
            ):
                with dpg.table(header_row=False):
                    # Three columns and two rows for six data types.
                    for _ in range(3):
                        dpg.add_table_column()
                    for j in range(1,4):
                        # Plot tag is 'data_typedancer_sensorcoordinate'
                        with dpg.table_row():
                            # Plot for acceleration data.
                            with dpg.plot(
                                tag=f'dncr{i+1}_snsr{j}_acc',
                                label='Waiting for id...'
                            ):
                                dpg.add_plot_legend()
                                dpg.add_plot_axis(dpg.mvXAxis)
                                item = dpg.add_plot_axis(dpg.mvYAxis)
                                # Acceleration data in x axis direction.
                                dpg.add_line_series(
                                    x_axis, initial_data, label='x', 
                                    tag=f'acc{i}_{j}x', parent=dpg.last_item()
                                )
                                dpg.set_axis_limits(item, 0, 1)
                                item = dpg.add_plot_axis(dpg.mvYAxis)
                                # Acceleration data in y axis direction.
                                dpg.add_line_series(
                                    x_axis, initial_data, label='y', 
                                    tag=f'acc{i}_{j}y', parent=dpg.last_item()
                                )
                                dpg.set_axis_limits(item, 0, 1)
                                item = dpg.add_plot_axis(dpg.mvYAxis)
                                # Acceleration data in z axis direction.
                                dpg.add_line_series(
                                    x_axis, initial_data, label='z', 
                                    tag=f'acc{i}_{j}z', parent=dpg.last_item()
                                )
                                dpg.set_axis_limits(item, 0, 1)
                            # Plot for total acceleration data.
                            with dpg.plot(
                                tag=f'dncr{i+1}_snsr{j}_tot_a',
                                label='Waiting for id...'
                                ):
                                dpg.add_plot_legend()
                                dpg.add_plot_axis(dpg.mvXAxis)
                                item = dpg.add_plot_axis(dpg.mvYAxis)
                                # Total acceleration data.
                                dpg.add_line_series(
                                    x_axis, initial_data, label='acc', 
                                    tag=f'tot_a{i}_{j}', parent=dpg.last_item()
                                )
                                dpg.set_axis_limits(item, 0, 50)
                                dpg.add_drag_line(
                                    default_value=30, vertical=False,
                                    label="threshold", color=[255, 0, 0, 255],
                                    callback=self.set_threshold
                                )
                                item = dpg.add_plot_axis(
                                    dpg.mvYAxis, label='bin'
                                )
                                # Total acceleration binary data.
                                dpg.add_line_series(
                                    x_axis, initial_data, label='0/1', 
                                    tag=f'b_tot_a{i}_{j}', 
                                    parent=dpg.last_item()
                                )
                                dpg.set_axis_limits(item, 0, 1)
                            # Plot for orientation data.
                            with dpg.plot(
                                tag=f'dncr{i+1}_snsr{j}_ori',
                                label='Waiting for id...'
                                ):
                                dpg.add_plot_legend()
                                dpg.add_plot_axis(dpg.mvXAxis)
                                item = dpg.add_plot_axis(dpg.mvYAxis)
                                # Orientation data in x axis direction.
                                dpg.add_line_series(
                                    x_axis, initial_data, label='pitch', 
                                    tag=f'ori{i}_{j}p', parent=dpg.last_item()
                                )
                                dpg.set_axis_limits(item, -180, 180)
                                item = dpg.add_plot_axis(dpg.mvYAxis)
                                # Orientation data in y axis direction.
                                dpg.add_line_series(
                                    x_axis, initial_data, label='roll', 
                                    tag=f'ori{i}_{j}r', parent=dpg.last_item()
                                )
                                dpg.set_axis_limits(item, -180, 180)
                                item = dpg.add_plot_axis(dpg.mvYAxis)
                                # Orientation data in z axis direction.
                                dpg.add_line_series(
                                    x_axis, initial_data, label='yaw', 
                                    tag=f'ori{i}_{j}y', parent=dpg.last_item()
                                )
                                dpg.set_axis_limits(item, -180, 180)
                        with dpg.table_row():
                            # Plot for gyroscope data.
                            with dpg.plot(
                                tag=f'dncr{i+1}_snsr{j}_gyr',
                                label='Waiting for id...'
                                ):
                                dpg.add_plot_legend()
                                dpg.add_plot_axis(dpg.mvXAxis)
                                item = dpg.add_plot_axis(dpg.mvYAxis)
                                # Gyroscope data in x axis direction.
                                dpg.add_line_series(
                                    x_axis, initial_data, label='x', 
                                    tag=f'gyr{i}_{j}x', parent=dpg.last_item()
                                )
                                dpg.set_axis_limits(item, 0, 1)
                                item = dpg.add_plot_axis(dpg.mvYAxis)
                                # Gyroscope data in y axis direction.
                                dpg.add_line_series(
                                    x_axis, initial_data, label='y', 
                                    tag=f'gyr{i}_{j}y', parent=dpg.last_item()
                                )
                                dpg.set_axis_limits(item, 0, 1)
                                item = dpg.add_plot_axis(dpg.mvYAxis)
                                # Gyroscope data in z axis direction.
                                dpg.add_line_series(
                                    x_axis, initial_data, label='z', 
                                    tag=f'gyr{i}_{j}z', parent=dpg.last_item()
                                )
                                dpg.set_axis_limits(item, 0, 1)
                            # Plot for rate of turn data.
                            with dpg.plot(
                                tag=f'dncr{i+1}_snsr{j}_rot',
                                label='Waiting for id...'
                                ):
                                dpg.add_plot_legend()
                                dpg.add_plot_axis(dpg.mvXAxis)
                                item = dpg.add_plot_axis(dpg.mvYAxis)
                                # Rate of turn data.
                                dpg.add_line_series(
                                    x_axis, initial_data, label='rot', 
                                    tag=f'rot{i}_{j}', parent=dpg.last_item()
                                )
                                dpg.set_axis_limits(item, 0, 1)
                            # Plot for magnetomter data.
                            with dpg.plot(
                                tag=f'dncr{i+1}_snsr{j}_mag',
                                label='Waiting for id...'
                                ):
                                dpg.add_plot_legend()
                                dpg.add_plot_axis(dpg.mvXAxis)
                                item = dpg.add_plot_axis(dpg.mvYAxis)
                                # X-axis magnetomter data.
                                dpg.add_line_series(
                                    x_axis, initial_data, label='x', 
                                    tag=f'mag{i}_{j}x', parent=dpg.last_item()
                                )
                                dpg.set_axis_limits(item, 0, 1)
                                item = dpg.add_plot_axis(dpg.mvYAxis)
                                # Y-axis magnetomter data.
                                dpg.add_line_series(
                                    x_axis, initial_data, label='y', 
                                    tag=f'mag{i}_{j}y', parent=dpg.last_item()
                                )
                                dpg.set_axis_limits(item, 0, 1)
                                item = dpg.add_plot_axis(dpg.mvYAxis)
                                # Z-axis magnetomter data.
                                dpg.add_line_series(
                                    x_axis, initial_data, label='z', 
                                    tag=f'mag{i}_{j}z', parent=dpg.last_item()
                                )
                                dpg.set_axis_limits(item, 0, 1)
        # File dialog for selecting a log file for plotting.
        with dpg.file_dialog(
            directory_selector=False, show=False,
            callback=self.file_dialog_callback,
            tag='file_dialog',
            width=800 ,height=500
        ):
            dpg.add_file_extension('.txt', color=(0, 255, 0, 255))
