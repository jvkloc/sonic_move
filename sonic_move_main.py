# Sonic Move Biodata Sonata main script.
import sys
import argparse
# Xsens Device API documentation provided with SDK download:
# https://www.movella.com/support/software-documentation.
import xsensdeviceapi as xda
# https://dearpygui.readthedocs.io/en/latest/
import dearpygui.dearpygui as dpg

import dashboard as db
import xda_device as xd
import sensors as ss
import osc


def recording_loop():
    pass


def main():
    """Sonic Move Biodata Sonata main function. Xsens Device API
    library is written in mixedCase style which clashes with Dear
    PyGui's lower_case_with_underscores. The latter style is
    easier to read so also Sonic Move Biodata Sonata Python
    scripts are written using it. For usability it is probably the
    best to set your own defaults for the main function
    arguments, instead of typing them every time separately.
    Arguments
    --------------
    device : str
        'dongle' or 'station', default is 'dongle'.
    path : str
        The file path for log files created by the script.
    server_ip :
        Open Sound Control server IP address.
    server_port :
        Open Sound Control port.
    client_ip :
        Open Sound Control client IP address.
    client_port :
        Open Sound Control client port.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--device', '-d', type=str, default='dongle',
        help='"dongle" or "station"'
        )
    parser.add_argument(
        '--path', '-p', type=str,
        default='/path/to/log/file/',
        help='Path for log files.'
    )
    parser.add_argument(
        '--server_ip', '-si', type=str, default='127.0.0.1',
        help='OSC server IP.'
    )
    parser.add_argument(
        '--server_port', '-sp', type=int, default=50005,
        help='OSC server port.'
    )
    parser.add_argument(
        '--client_ip', '-ci', type=str, default='127.0.0.1',
        help='OSC client IP.'
    )
    parser.add_argument(
        '--client_port', '-cp', type=int, default=50005,
        help='OSC client port.'
    )
    args = parser.parse_args()

    try:
        dashboard = db.Dashboard()
    except Exception as e:
        print(f'{e}. Dashboard setup failed. Aborting.')
        sys.exit(1)
    try:
        main_device = xd.XdaDevice(args[0])
        main_device.create_control_object()
        main_device.open_device()
        main_device.configure_device(args[1])
    except Exception as e:
        dpg.set_value(
            'program_status', f'{e}. Main device setup failed. Aborting.'
            f'\n\n{dpg.get_value("program_status")}'
        )
        print(f'{e}. Main device setup failed. Aborting')
        sys.exit(1)
    try:
        osc('127.0.0.1', 50005, '127.0.0.1', 50005)
    except Exception as e:
        dpg.set_value(
            'program_status', f'{e}. Open Sound Control setup failed.'
            f' Aborting.\n\n{dpg.get_value("program_status")}'
        )
        print(f'{e}. Open Sound Control setup failed. Aborting')
        sys.exit(1)

    main_device.record()

if __name__ == "__main__":
    main()
