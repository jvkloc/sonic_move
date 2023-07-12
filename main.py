# Script for live Awinda MTw2 sensors with Awinda2 USB Dongle.
import sys
# Xsens Device API documentation provided with SDK download:
# https://www.movella.com/support/software-documentation.
import xsensdeviceapi as xda
# https://dearpygui.readthedocs.io/en/latest/
import dearpygui.dearpygui as dpg

from GUI import GUI
from XdaDevice import XdaDevice
from Sensors import Sensors
from OSC import OSC

def main(device='dongle', log_path='/home/file/path/'):
    """Sonic Move main script.
    Parameters
    --------------
    device : str
        'dongle' or 'station', default is 'dongle'.
    log_path : str
        The file path for log files created by the script.
    """
    args = sys.argv[1:]
    dashboard = GUI()

    dpg.set_value(
        'program_status', 'Creating an XsControl object...\n'
    )
    print('Creating an XsControl object... ')
    control = xda.XsControl()
    xda_version = xda.XsVersion()
    xda.xdaVersion(xda_version)
    if control != 0:
        dpg.set_value(
            'program_status', 'XsControl object created successfully.\n'
            f'Xsens Device API version: {xda_version.toXsString()}\n'
            f'{dpg.get_value("program_status")}'
        )
        print(
            'XsControl object created successfully.\n'
            f'Xsens Device API version: {xda_version.toXsString()}\n'
        )

    try:
        main_device = XdaDevice(control, args[0])
        main_device.setDevice()
        main_device.configureDevice()
        main_device.setMTw2s()
        #main_device.setMTw2Locations()
        main_device.preRecordingMode(args[1])
    except Exception as e:
        dpg.set_value(
            'program_status', f'{e}. Main device setup failed. Aborting.'
            f'\n\n{dpg.get_value("program_status")}'
        )
        print(f'{e}. Main device setup failed. Aborting')
        sys.exit(1)

    try:
        sensors = Sensors()
        sensors.status(main_device.MTw2s, ids=True)
        sensors.set_ids(main_device.MTw2_ids)
    except Exception as e:
        dpg.set_value(
            'program_status', f'{e}. Sensor setup failed. Aborting.\n\n'
            f'{dpg.get_value("program_status")}'
        )
        print(f'{e}. Sensor setup failed. Aborting')
        sys.exit(1)

    try:
        open_sound_control = OSC()
    except Exception as e:
        dpg.set_value(
            'program_status', f'{e}. OSC setup failed. Aborting.\n\n'
            f'{dpg.get_value("program_status")}'
        )
        print(f'{e}. OSC setup failed. Aborting')
        sys.exit(1)

    main_device.setRecording()
    main_device.recordingLoop(dashboard.recording)
