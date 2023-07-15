# A class for Sonic Move DearPyGUI dashboard.
import threading
# https://dearpygui.readthedocs.io/en/latest/
import dearpygui.dearpygui as dpg
import dancers as ds


class Dashboard:
    """Class for Sonic Move Biodata Sonate dashboard.
    Argument and function names describe what is happening.
    A few additional comments have been added for readability.
    """
    def __init__(self):
        """
        Attributes
        ------------
        recording : boolean
            A boolean for checking the recording loop condition.
        acc_threshold : int
            Default is 30 m/s**2 for a total acceleration 'hit'.
        dancers : list
            List of dictionaries of dictionaries. Identical to Sensors
            class self.dancers, needed for initialising the dashboard.
            Not used in any other context.
        """
        self.recording = False
        self.acc_threshold = 30
        self.dancers = ds.Dancers()
        self.setup()

    def toggle_recording(self, sender, app_data):
        """recording switches recording on and off. """
        self.recording = not self.recording
        #threading.Thread(target=main, daemon=True).start()
        #if self.recording:


    def set_threshold(self, sender, data):
        """set_threshold sets the total acceleration threshold
        from the GUI total acceleration plot horizontal bar.
        """
        self.acc_threshold = dpg.get_value(sender)

    def setup(self):
        """setup creates a Dear PyGUI dashboard. """
        dpg.create_context()
        vp = dpg.create_viewport(title='Sonify dashboard')
        vp_width = dpg.get_viewport_width()
        window_lbl = ['one', 'two', 'three']
        window_pos = [(45,300), (25,320), (5,340)]
        x_axis = list(range(500))
        # Create program status display window.
        with dpg.window(
            label='Recording panel', pos=(25,0),
            width=vp_width
        ):
            dpg.add_button(
                label='Recording on/off',
                callback=self.toggle_recording
            )
            dpg.add_text(
                'Use mouse to scroll down program message history. First'
                ' message is in the bottom row.'
            )
            dpg.add_input_text(
                tag='program_status', width=vp_width, multiline=True
            )
        # Create sensor status display window.
        with dpg.window(
            label='Sensor status panel', pos=(25,195),
            width=vp_width
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
                'Click on plot legend variables to show or hide related'
                ' data'
            )
        # Create a window for sensors of each dancer.
        for i in range(3):
            w = dpg.add_window( # Attribute error: __enter__
                label=f'Dancer {window_lbl[i]}', pos=window_pos[i],
                width=vp_width, collapsed=True
            )
            with dpg.table(parent=w, header_row=False):
                # Three columns and two rows for six data types.
                for _ in range(3):
                    dpg.add_table_column()
                for j in range(3):
                    # Plot tag is 'data_typedancer_sensorcoordinate'
                    with dpg.table_row():
                        # Create plot for acceleration data.
                        with dpg.plot(
                            tag=f'dncr{i+1}_snsr{j+1}_acc',
                            label='Waiting for id...'
                        ):
                            dpg.add_plot_legend()
                            dpg.add_plot_axis(dpg.mvXAxis)
                            item = dpg.add_plot_axis(dpg.mvYAxis)
                            # Add acceleration data in x axis direction.
                            dpg.add_line_series(
                                x_axis,
                                self.dancers.dancers[i][f'snsr_{j+1}']['acc_x'],
                                label='x', tag=f'acc{i}_{j+1}x',
                                parent=dpg.last_item()
                            )
                            dpg.set_axis_limits(item, 0, 1)
                            item = dpg.add_plot_axis(dpg.mvYAxis)
                            # Add acceleration data in y axis direction.
                            dpg.add_line_series(
                                x_axis,
                                self.dancers.dancers[i][f'snsr_{i+1}']['acc_y'],
                                label='y', tag=f'acc{i}_{j+1}y',
                                parent=dpg.last_item()
                            )
                            dpg.set_axis_limits(item, 0, 1)
                            item = dpg.add_plot_axis(dpg.mvYAxis)
                            # Add acceleration data in z axis direction.
                            dpg.add_line_series(
                                x_axis,
                                self.dancers.dancers[i][f'snsr_{j+1}']['acc_z'],
                                label='z', tag=f'acc{i}_{j+1}z',
                                parent=dpg.last_item()
                            )
                            dpg.set_axis_limits(item, 0, 1)
                        # Create plot for total acceleration data.
                        with dpg.plot(
                            tag=f'dncr{i+1}_snsr{j+1}_tot_a',
                            label='Waiting for id...'
                        ):
                            dpg.add_plot_legend()
                            dpg.add_plot_axis(dpg.mvXAxis)
                            item = dpg.add_plot_axis(dpg.mvYAxis)
                            # Add total acceleration data.
                            dpg.add_line_series(
                                x_axis,
                                self.dancers.dancers[i][f'snsr_{j+1}']['tot_a'],
                                label='acc', tag=f'tot_a{i}_{j+1}',
                                parent=dpg.last_item()
                            )
                            dpg.set_axis_limits(item, 0, 50)
                            dpg.add_drag_line(
                                default_value=30, vertical=False,
                                label="threshold", color=[255, 0, 0, 255],
                                callback=self.set_threshold
                            )
                            item = dpg.add_plot_axis(dpg.mvYAxis, label='bin')
                            # Add total acceleration binary data.
                            dpg.add_line_series(
                                x_axis,
                                self.dancers.dancers[i][f'snsr_{j+1}']['b_tot_a'],
                                label='0/1', tag=f'bin_tot_a{i}_{j+1}',
                                parent=dpg.last_item()
                            )
                            dpg.set_axis_limits(item, 0, 1)
                        # Create plot for orientation data.
                        with dpg.plot(
                            tag=f'dncr{i+1}_snsr{j+1}_ori',
                            label='Waiting for id...'
                        ):
                            dpg.add_plot_legend()
                            dpg.add_plot_axis(dpg.mvXAxis)
                            item = dpg.add_plot_axis(dpg.mvYAxis)
                            # Add orientation data in x axis direction.
                            dpg.add_line_series(
                                x_axis,
                                self.dancers.dancers[i][f'snsr_{j+1}']['ori_p'],
                                label='pitch', tag=f'ori{i}_{j+1}p',
                                parent=dpg.last_item()
                            )
                            dpg.set_axis_limits(item, -180, 180)
                            item = dpg.add_plot_axis(dpg.mvYAxis)
                            # Add orientation data in y axis direction.
                            dpg.add_line_series(
                                x_axis,
                                self.dancers.dancers[i][f'snsr_{j+1}']['ori_r'],
                                label='roll', tag=f'ori{i}_{j+1}r',
                                parent=dpg.last_item()
                            )
                            dpg.set_axis_limits(item, -180, 180)
                            item = dpg.add_plot_axis(dpg.mvYAxis)
                            # Add orientation data in z axis direction.
                            dpg.add_line_series(
                                x_axis,
                                self.dancers.dancers[i][f'snsr_{j+1}']['ori_y'],
                                label='yaw', tag=f'ori{i}_{j+1}y',
                                parent=dpg.last_item()
                            )
                            dpg.set_axis_limits(item, -180, 180)
                    with dpg.table_row():
                        # Create plot for gyroscope data.
                        with dpg.plot(
                            tag=f'dncr{i+1}_snsr{j+1}_gyr',
                            label='Waiting for id...'
                        ):
                            dpg.add_plot_legend()
                            dpg.add_plot_axis(dpg.mvXAxis)
                            item = dpg.add_plot_axis(dpg.mvYAxis)
                            # Add gyroscope data in x axis direction.
                            dpg.add_line_series(
                                x_axis,
                                self.dancers.dancers[i][f'snsr_{j+1}']['gyr_x'],
                                label='x', tag=f'gyr{i}_{j+1}x',
                                parent=dpg.last_item()
                            )
                            dpg.set_axis_limits(item, 0, 1)
                            item = dpg.add_plot_axis(dpg.mvYAxis)
                            # Add gyroscope data in y axis direction.
                            dpg.add_line_series(
                                x_axis,
                                self.dancers.dancers[i][f'snsr_{j+1}']['gyr_y'],
                                label='y', tag=f'gyr{i}_{j+1}y',
                                parent=dpg.last_item()
                            )
                            dpg.set_axis_limits(item, 0, 1)
                            item = dpg.add_plot_axis(dpg.mvYAxis)
                            # Add gyroscope data in z axis direction.
                            dpg.add_line_series(
                                x_axis,
                                self.dancers.dancers[i][f'snsr_{j+1}']['gyr_z'],
                                label='z', tag=f'gyr{i}_{j+1}z',
                                parent=dpg.last_item()
                            )
                            dpg.set_axis_limits(item, 0, 1)
                            # Create plot for rate of turn data.
                        with dpg.plot(
                            tag=f'dncr{i+1}_snsr{j+1}_rot',
                            label='Waiting for id...'
                        ):
                            dpg.add_plot_legend()
                            dpg.add_plot_axis(dpg.mvXAxis)
                            item = dpg.add_plot_axis(dpg.mvYAxis)
                            # Add rate of turn data.
                            dpg.add_line_series(
                                x_axis,
                                self.dancers.dancers[i][f'snsr_{j+1}']['rot'],
                                label='rot', tag=f'rot{i}_{j+1}',
                                parent=dpg.last_item()
                            )
                            dpg.set_axis_limits(item, 0, 1)
                        # Create plot for magnetomter data.
                        with dpg.plot(
                            tag=f'dncr{i+1}_snsr{j+1}_mag',
                            label='Waiting for id...'
                        ):
                            dpg.add_plot_legend()
                            dpg.add_plot_axis(dpg.mvXAxis)
                            item = dpg.add_plot_axis(dpg.mvYAxis)
                            # Add x axis magnetomter data.
                            dpg.add_line_series(
                                x_axis,
                                self.dancers.dancers[i][f'snsr_{j+1}']['mag_x'],
                                label='x', tag=f'mag{i}_{j+1}x',
                                parent=dpg.last_item()
                            )
                            dpg.set_axis_limits(item, 0, 1)
                            item = dpg.add_plot_axis(dpg.mvYAxis)
                            # Add y axis magnetomter data.
                            dpg.add_line_series(
                                x_axis,
                                self.dancers.dancers[i][f'snsr_{j+1}']['mag_y'],
                                label='y', tag=f'mag{i}_{j+1}y',
                                parent=dpg.last_item()
                            )
                            dpg.set_axis_limits(item, 0, 1)
                            item = dpg.add_plot_axis(dpg.mvYAxis)
                            # Add z axis magnetomter data.
                            dpg.add_line_series(
                                x_axis,
                                self.dancers.dancers[i][f'snsr_{j+1}']['mag_z'],
                                label='z', tag=f'mag{i}_{j+1}z',
                                parent=dpg.last_item()
                            )
                            dpg.set_axis_limits(item, 0, 1)

        dpg.setup_dearpygui()
        dpg.maximize_viewport()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()
