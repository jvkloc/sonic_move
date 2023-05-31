# program code for reading live Awinda MTw2 sensors through Awinda2 USB Dongle
import xsensdeviceapi as xda # documentation provided with SDK download
import XdaCallback as xc
import sonify_functions as sf
import dearpygui.dearpygui as dpg
from osc4py3 import oscmethod as osm # https://osc4py3.readthedocs.io/en/latest/
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse
from math import sqrt, floor
import threading
import logging
import time
import sys
# ################################################################################################################
# set filepath for log file: see line 167
log_path = ''
# variables for total acceleration timeout on lines 198-200
# set Open Sound Control IP addresses (string) and ports (int) for sending OSC messages: see lines 190-195
osc_server_ip = '' 
osc_server_port = 0
osc_client_ip = ''
osc_client_port = 0
# set variable for total acceleration threshold (m/s**2)
acc_treshold = 30
# ################################################################################################################
# variable for stopping recording
stop_rec = False
# dpg callback for starting recording
def start(sender, app_data):
    global stop_rec
    stop_rec = False
    threading.Thread(target=sonify_main, daemon=True).start()
# dpg callback for stopping recording
def stop(sender, app_data):
    global stop_rec
    stop_rec = True
# function for setting the total acceleration threshold
def set_threshold(sender, data):
    global acc_threshold 
    acc_threshold = dpg.get_value(sender)
# main script   
def sonify_main():
    # create a Xsens device management object and print API version info to the user
    dpg.set_value('program_status', 'Creating an XsControl object...\n')
    print('Creating an XsControl object... ')
    control = xda.XsControl()
    xda_version = xda.XsVersion()
    xda.xdaVersion(xda_version)
    if control != 0:
        dpg.set_value('program_status', 'XsControl object created successfully.\nXsens Device API version: ' + xda_version.toXsString() + '\n' + f'{dpg.get_value("program_status")}')
        print('XsControl object created successfully.\nXsens Device API version: ' + xda_version.toXsString() + '\n')
    try:        
        # get the available ports and master devices
        dpg.set_value('program_status', 'Scanning for ports with Xsens devices...\n' + f'{dpg.get_value("program_status")}')
        print('Scanning for ports with Xsens devices...')
        port_info = xda.XsScanner_scanPorts()
        # print port info or exit if no Xsens devices are connected
        if len(port_info) != 0:
            dpg.set_value('program_status', 'The following ports with a connected Xsens device were found:\n' + f'{dpg.get_value("program_status")}')
            print('The following ports with a connected Xsens device were found:')
            for port in port_info:
                dpg.set_value('program_status', port.portName() + f' with baud rate {port.baudrate()} Bd and device id {port.deviceId()}\n' + f'{dpg.get_value("program_status")}')
                print(port.portName() + f' with baud rate {port.baudrate()} Bd and device id {port.deviceId()}')
        else:
            dpg.set_value('program_status', 'SystemExit: No devices found.\n\n' + f'{dpg.get_value("program_status")}')
            raise RuntimeError('SystemExit: No devices found.')
        # get the Awinda Dongles connected to the ports or exit if the devices are of another type
        dngl_ports = []
        dpg.set_value('program_status', 'Checking the type of the connected Xsens devices...\n\n' + f'{dpg.get_value("program_status")}')
        print('\nChecking the type of the connected Xsens devices...')
        for port in port_info:
            if port.deviceId().isAwinda2Dongle():
                dngl_ports.append(port)
                dpg.set_value('program_status', 'Device ' + str(port.deviceId()) + ' is of type AW-DNG2\n' + f'{dpg.get_value("program_status")}')
                print('Device ' + str(port.deviceId()) + ' is of type AW-DNG2')
        if len(dngl_ports) == 0:
            dpg.set_value('program_status', 'No AW-DNG2 devices found. Aborting.\n\n' + f'{dpg.get_value("program_status")}')
            raise RuntimeError('No AW-DNG2 devices found. Aborting.')
        # open the ports of the Awinda Dongles (assuming only one device in one port)
        devices = []
        dpg.set_value('program_status', 'Opening the ports of the Xsens devices...\n\n' + f'{dpg.get_value("program_status")}')
        print('\nOpening the ports of the Xsens devices...')
        for port in dngl_ports: 
            if not control.openPort(port.portName(), port.baudrate()):
                dpg.set_value('program_status', 'RuntimeError: Aborting.\n\n' + f'{dpg.get_value("program_status")}')
                raise RuntimeError('RuntimeError: Aborting.')    
            # use the Awinda Dongle ids to initialise contol object devices and notify the user
            devices.append(control.device(port.deviceId()))
            dpg.set_value('program_status', 'Port ' + port.portName() + f' for AW-DNG2 {port.deviceId().toXsString()} opened\n' + f'{dpg.get_value("program_status")}')
            print('Port ' + port.portName() + f' for AW-DNG2 {port.deviceId().toXsString()} opened')
        # implement recording 
        #print('\nSet radio channel and update rate for the connected devices.')
        chnls = ' '.join(map(str, list(range(11,26))))
        reserved_chnls = []
        #print('Available radio channels are ' + chnls + '.')
        #print('Recommended wireless update rates are:')
        #print('  60Hz for 11 - 20 MTw sensors\n  80Hz for     10    MTw sensors\n100Hz for   6 - 9   MTw sensors\n120Hz for   1 - 5   MTw sensors')
        # array for connected MTw2 sensors (assuming only one Dongle)
        mtw2s = []
        # array for connected MTw2 sensors' ids
        mtw2_ids = []
        for device in devices:
            # set callback handlers to the Dongle
            callback = xc.XdaCallback()
            device.addCallbackHandler(callback)
            # set the Dongle to record live data
            device.setOptions(xda.XSO_RetainLiveData or xda.XSO_Orientation or XSO_OrientationInLiveStream, xda.XSO_None)
            # choose and set update rates and choose radio channels
            device.gotoConfig()
            try:
                update_rates = device.supportedUpdateRates(xda.XSO_None)
            except:
                dpg.set_value('program_status', 'Failed to get supported update rates for AW-DNG2 {device.deviceId()}. Aborting.\n\n' + f'{dpg.get_value("program_status")}')
                print(f'Failed to get supported update rates for AW-DNG2 {device.deviceId()}. Aborting.')
                sys.exit(1)
            rates = 'Hz '.join(map(str, update_rates)) + 'Hz'    
            #print(f'\nSupported update rates for AW-DNG2 {device.deviceId()}: {rates}')
            #selected_rate = int(input(f'Select one of the supported update rates for AW-DNG2 {device.deviceId()}: '))
            #radio_chnl = int(input(f'Select one of the available radio channels AW-DNG2 {device.deviceId()}: '))
            selected_rate = 100 # hardcoded for Minimi's Biodata Sonate project
            radio_chnl = 11 # hardcoded for Minimi's Biodata Sonate project
            if selected_rate in update_rates:
                device.setUpdateRate(selected_rate)
            else:
                dpg.set_value('program_status', 'The selected update rate is not supported.Aborting\n\n' + f'{dpg.get_value("program_status")}')
                print('The selected update rate is not supported. Aborting.')
                sys.exit(1)
            # enable radios
            if radio_chnl not in reserved_chnls:
                device.enableRadio(radio_chnl)
                reserved_chnls.append(radio_chnl)
                dpg.set_value('program_status', f'AW-DNG2 {device.deviceId()} update rate set to {selected_rate} Hz and radio enabled on channel {radio_chnl}\n' + f'{dpg.get_value("program_status")}')
                print(f'AW-DNG2 {device.deviceId()} update rate set to {selected_rate} Hz and radio enabled on channel {radio_chnl}')
            # wait for the MTw2 sensors to connect
            dpg.set_value('program_status', f'Connecting the MTw2 sensors to AW-DNG2 {device.deviceId()}...\n\n' + f'{dpg.get_value("program_status")}')
            print(f'\nConnecting the MTw2 sensors to AW-DNG2 {device.deviceId()}...')
            time.sleep(5)
            # confirm that the MTw2 sensors are connected
            dpg.set_value('program_status', f'{device.childCount()} MTw2 sensors connected to AW-DNG2 {device.deviceId()} initialised\n' + f'{dpg.get_value("program_status")}')
            print(f'{device.childCount()} MTw2 sensors connected to AW-DNG2 {device.deviceId()} initialised')
            dpg.set_value('program_status', 'Configuring the connected MTw2 sensors...\n' + f'{dpg.get_value("program_status")}')
            print('Configuring the connected MTw2 sensors...')
            # configuration arrays for the attached MTw2 sensors
            for mtw in device.children():
               # save MTw2 sensors and ids
                mtw2_ids.append(f'{mtw.deviceId()}')
                mtw2s.append(mtw)
                # add configuration for data types
                mtw.gotoConfig()
                config_array = xda.XsOutputConfigurationArray()
                config_array.push_back(xda.XsOutputConfiguration(xda.XDI_PacketCounter, 0))
                config_array.push_back(xda.XsOutputConfiguration(xda.XDI_SampleTimeFine, 0)) 
                config_array.push_back(xda.XsOutputConfiguration(xda.XDI_Acceleration, 0xFFFF))
                config_array.push_back(xda.XsOutputConfiguration(xda.XDI_EulerAngles, 0xFFFF))
                # set the array to the MTw2
                if not mtw.setOutputConfiguration(config_array):
                    dpg.set_value('program_status', f'Configuration of MTw2 sensor {mtw.deviceId()} failed. Aborting.\n\n' + f'{dpg.get_value("program_status")}')
                    raise RuntimeError(f'Configuration of MTw2 sensor {mtw.deviceId()} failed. Aborting.')
            # set the Dongle and connected sensors to measurement mode
            if not device.gotoMeasurement():
                dpg.set_value('program_status', f'Failed to set AW-DNG2 {device.deviceId()} to measurement mode. Aborting.\n\n' + f'{dpg.get_value("program_status")}')
                raise RuntimeError(f'Failed to set AW-DNG2 {device.deviceId()} to measurement mode. Aborting.')
            # check that the MTw2s are in measurement mode
            for mtw in device.children():
                if mtw.isMeasuring():
                    dpg.set_value('program_status', f'MTw2 {mtw.deviceId()} connected to AW-DNG2 {device.deviceId()} set to measurement mode\n' + f'{dpg.get_value("program_status")}')
                    print(f'MTw2 {mtw.deviceId()} connected to AW-DNG2 {device.deviceId()} set to measurement mode')
            # create log file
            dpg.set_value('program_status', f'Creating a log file for AW-DNG2 {device.deviceId()} and starting recording...\n\n' + f'{dpg.get_value("program_status")}')
            print(f'\nCreating a log file for AW-DNG2 {device.deviceId()} and starting recording...')
            log = f'{log_path}{device.deviceId()}_log.mtb'
            if device.createLogFile(log) != xda.XRV_OK:
                dpg.set_value('program_status', f'Failed to create a log file for AW-DNG2 {device.deviceId()}. Aborting.\n\n' + f'{dpg.get_value("program_status")}')
                raise RuntimeError(f'Failed to create a log file for AW-DNG2 {device.deviceId()}. Aborting.')
            # start recording
            try:
                device.startRecording() 
                dpg.set_value('program_status', f'AW-DNG {device.deviceId()} is recording the connected MTw2 sensors\n' + f'{dpg.get_value("program_status")}')
                print(f'AW-DNG {device.deviceId()} is recording the connected MTw2 sensors')
            except: 
                dpg.set_value('program_status', f'AW-DNG {device.deviceId()} failed to start recording. Aborting.\n\n' + f'{dpg.get_value("program_status")}')
                print(f'AW-DNG {device.deviceId()} failed to start recording. Aborting.')
                sys.exit(1)      
        # set a logger
        logging.basicConfig(format='%(asctime)s - %(processName)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARNING)
        logger = logging.getLogger('logger')            
        # install the osc4py3 tools
        osc_startup(logger=logger)
        # create osc4py3 server for testing the OSC messages sent by OSC client: ip, port, name
        osc_udp_server(osc_server_ip, osc_server_port, 'OSC_server')
        # set handler function for osc4py3 messages
        osc_method('/test/*', sf.handler)
        # create osc4py3 client: ip, port, name
        osc_udp_client(osc_client_ip, osc_client_port, 'OSC_client') 
        dpg.set_value('program_status', 'Use dashboard "stop recording" button to stop\n\n' + f'{dpg.get_value("program_status")}')
        print('Use dashboard "stop recording" button to stop\n')
        # variables for total acceleration binary display
        count_from = 0  # set timeout counter
        timeout = 0.2 # seconds timeout during which the program does not register a new hit from acceleration 
        # create dictionary for dancer number and body position of MTw2 sensors
        mtw2_locations = {}
        locations = ['left', 'right', 'middle']
        # place MTw2 sensors in order dancer one, left, right, middle and similarly for dancers two and three
        for i in range(len(mtw2_ids)): 
            # second value is for Open Sound Control Message, lines 218-219
            mtw2_locations[mtw2_ids[i]] = [f'Dancer {floor(i/3)+1} {locations[i-floor(i/3)*3]}', f'{floor(i/3)+1}{i+1-floor(i/3)*3}']    
        # set MTw2 sensor status on the dashboard
        sf.status(mtw2s, mtw2_locations, ids=True)
        # set MTw2 sensor ids to dashboard plots and normalisation dictionary
        sf.set_sensor_ids(mtw2_ids, mtw2_locations) 
        while not stop_rec: 
            # message variable for sending MTw2 sensor data to Open Sound Control environment
            osc_msg = []
            # check if a data packet is available
            if callback.packetAvailable():
                # get the data packet
                packet = callback.getNextPacket()
                # check if MTw2 id from which the packet is is available
                if packet.containsStoredDeviceId():
                    # append MTw2 id for Open Sound Control message
                    mtw2_id = f'{packet.deviceId()}' 
                    # xy where x is dancer number and y is 1 for left, 2 for right and 3 for middle
                    osc_msg.append(mtw2_locations[mtw2_id][1]) 
                # check for calibrated data
                if packet.containsCalibratedData():
                    # get acceleration data 
                    acc = packet.calibratedAcceleration()
                    acc_value = sf.normalise(mtw2_id, 'acc', [acc[0], acc[1], acc[2]])
                    # get total acceleration as Euclidean norm of acceleration
                    #tot_a_value = sf.normalise(mtw2_id, 'tot_a', [sqrt(acc[0]**2 + acc[1]**2 + acc[2]**2)]) 
                    # set total acceleration to 1 or 0 with chosen threshold and timeout
                    if sqrt(acc[0]**2 + acc[1]**2 + acc[2]**2) > acc_treshold and time.time() - count_from > timeout:
                        # first value is the measured total acceleration
                        tot_a_value = [sqrt(acc[0]**2 + acc[1]**2 + acc[2]**2), 1]
                        # set new time to count timeout from
                        count_from= time.time()
                    elif sqrt(acc[0]**2 + acc[1]**2 + acc[2]**2) <= acc_treshold:
                        # first value is the measured total acceleration
                        tot_a_value = [sqrt(acc[0]**2 + acc[1]**2 + acc[2]**2), 0]
                    # append acceleration data to Open Sound Control message
                    acc_value = [round(val, 5) for val in acc_value)]
                    osc_msg.append(acc_value)
                    osc_msg.append(round(tot_a_value[0], 5))
                    # send acceleration data to dashboard plot
                    sf.send_data(mtw2_id, mtw2_ids, 'acc', acc_value) 
                    sf.send_data(mtw2_id, mtw2_ids, 'tot_a', tot_a_value) 
                    # get gyroscope data
                    gyr = packet.calibratedGyroscopeData() 
                    gyr_value = sf.normalise(mtw2_id, 'gyr', [gyr[0], gyr[1], gyr[2]])                   
                    # get rate of turn from gyroscope data
                    rot_value = sf.normalise(mtw2_id, 'rot', [sqrt(gyr[0]**2 + gyr[1]**2 + gyr[2]**2)])                   
                    # append gyroscope and rate of turn data to Open Sound Control message
                    gyr_value = [round(val, 5) for val in gyr_value]
                    osc_msg.append(gyr_value)
                    osc_msg.append(rot_value[0])
                    # send gyroscope and rate of turn data to dashboard plot
                    sf.send_data(mtw2_id, mtw2_ids, 'gyr', gyr_value)
                    sf.send_data(mtw2_id, mtw2_ids, 'rot', rot_value)                        
                    # get magnetic field data 
                    mag = packet.calibratedMagneticField()
                    mag_value = [round(val, 5) for val in sf.normalise(mtw2_id, 'mag', [mag[0], mag[1], mag[2]])]                   
                    # append magnetic field data to Open Sound Control message
                    osc_msg.append(mag_value)
                    # send magnetic field data to dashboard plot
                    sf.send_data(mtw2_id, mtw2_ids, 'mag', mag_value)                       
                # check for orientation data 
                if packet.containsOrientation():
                    # get orientation data as Euler angles
                    euler = packet.orientationEuler() 
                    euler_value = [round(val, 5) for val in sf.normalise(mtw2_id, 'ori', [euler.x(), euler.y(), euler.z()])]                   
                    # append Euler angles data to Open Sound Control message
                    osc_msg.append(euler_value)                 
                    # send Euler angles data to dashboard plot
                    sf.send_data(mtw2_id, mtw2_ids, 'ori', euler_value)                               
                # send data from the data packet to Open Sound Control environment
                message = oscbuildparse.OSCMessage('/test/*', None, osc_msg)
                osc_send(message, 'OSC_client')
                osc_process()              
            # get measurement status of MTw2 sensors
            sf.status(mtw2s, mtw2_locations)                
        # uninstall the osc4py3 tools
        osc_terminate()
        # set measurement status of MTw2 sensors to 'Finished'
        sf.status(mtw2s, mtw2_locations, finished=True) 
        # stop recording and close all devices
        for device in devices:
            dpg.set_value('program_status', f'Closing AW-DNG2 {device.deviceId()}...\n' + f'{dpg.get_value("program_status")}')
            print(f'Closing AW-DNG2 {device.deviceId()}...')    
            try: 
                # stop recording
                device.stopRecording()
                dpg.set_value('program_status', f'AW-DNG2 {device.deviceId()} recording stopped...\n' + f'{dpg.get_value("program_status")}')
                print(f'AW-DNG2 {device.deviceId()} recording stopped', end='')
            except:
                dpg.set_value('program_status', f'Failed to stop AW-DNG2 {device.deviceId()} recording. Aborting.\n\n' + f'{dpg.get_value("program_status")}')
                print(f'\nFailed to stop AW-DNG2 {device.deviceId()} recording. Aborting.')
                sys.exit(1)
            # close log file
            if not device.closeLogFile():
                dpg.set_value('program_status', f'Failed to close AW-DNG2 {device.deviceId()} log file. Aborting.\n\n' + f'{dpg.get_value("program_status")}') 
                raise RuntimeError(f'\nFailed to close AW-DNG2 {device.deviceId()} log file. Aborting.')   
            dpg.set_value('program_status', '... and log file closed.\n' + f'{dpg.get_value("program_status")}')
            print(' and log file closed.')
            try:
                # remove callback handlers
                device.clearCallbackHandlers()
                dpg.set_value('program_status', f'AW-DNG2 {device.deviceId()} callback handler removed\n' + f'{dpg.get_value("program_status")}')
                print(f'AW-DNG2 {device.deviceId()} callback handler removed')
            except:
                dpg.set_value('program_status', f'Failed to remove callback handler from AW-DNG2 {device.deviceId()}. Aborting\n\n' + f'{dpg.get_value("program_status")}')
                print(f'Failed to remove callback handler from AW-DNG2 {device.deviceId()}. Aborting.')
                sys.exit(1)
            # disable radio
            device.disableRadio()
            dpg.set_value('program_status', f'AW-DNG2 {device.deviceId()} radio disabled\n' + f'{dpg.get_value("program_status")}')
            print(f'AW-DNG2 {device.deviceId()} radio disabled')
            dpg.set_value('program_status', f'All devices closed. Closing the ports...\n\n' + f'{dpg.get_value("program_status")}')
            print('\nAll devices closed. Closing the ports...')
        # close all ports
        for port in dngl_ports:
            control.closePort(port.portName())
            dpg.set_value('program_status', f'Port {port.portName()} closed\n' + f'{dpg.get_value("program_status")}')
            print(f'Port {port.portName()} closed')
        # close control object
        dpg.set_value('program_status', 'All ports closed. Closing the XsControl object...\n' + f'{dpg.get_value("program_status")}')
        print('All ports closed. Closing the XsControl object...')
        control.close()
        dpg.set_value('program_status', 'XsControl object closed\n' + f'{dpg.get_value("program_status")}')
        print('XsControl object closed')
    except RuntimeError as error:
        dpg.set_value('program_status', str(error) + f'Aborting.\n\n{dpg.get_value("program_status")}')
        print(error)
        sys.exit(1)
    except:
        dpg.set_value('program_status', 'Unknown error. Aborting.\n\n' + f'{dpg.get_value("program_status")}')
        print('Unknown error. Aborting.')
        sys.exit(1)
    else:
        dpg.set_value('program_status', 'Successful exit: ready for restart\n\n' + f'{dpg.get_value("program_status")}')
        print('Successful exit: ready for restart')
