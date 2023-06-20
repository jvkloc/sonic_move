# program code for reading live Awinda MTw2 sensors through Awinda2 USB Dongle
# Xsens Device API documentation provided with SDK download from https://www.movella.com/support/software-documentation
import xsensdeviceapi as xda 
import XdaDongle as xd
import sm_functions as sf
import dearpygui.dearpygui as dpg # https://dearpygui.readthedocs.io/en/latest/
from osc4py3.as_eventloop import * # https://osc4py3.readthedocs.io/en/latest/
from osc4py3 import oscbuildparse
from math import sqrt, floor
import threading
import logging
import time
import sys
# ###########################################################################################################################################
# set filepath for mtb log file, see XdaDongle.py line 160 (setRecording method)                                                                                                          
log_path = 'filepath'                                                                                                                    
# set Open Sound Control IP addresses (string) and ports (int) for sending OSC messages, see lines 76-88
osc_server_ip = '200'                                                                                                                                     
osc_server_port = 3000                                                                                                                                        
osc_client_ip = '100'                                                                                                                                      
osc_client_port = 5000                                                                                                                                         
# variable for total acceleration timeout on line 106, default 0.2 seconds                                                            
# set variable for total acceleration trigger threshold (m/s**2), see lines 128-136, sm_gui.py line 72, sm4col_gui.py lines 71, 169 and 268                                                  
acc_threshold = 30                                                                                                                                               
# ###########################################################################################################################################
# dpg callback for starting recording
def start(sender, app_data):
    global stop_rec
    stop_rec = False
    threading.Thread(target=main, daemon=True).start()
# dpg callback for stopping recording
def stop(sender, app_data):
    global stop_rec
    stop_rec = True
# dpg callback for setting the total acceleration threshold
def set_threshold(sender, data):
    global acc_threshold 
    acc_threshold = dpg.get_value(sender)
# variable for controlling recording
stop_rec = False
# main script   
def main():
    # create Xsens device management object and print API version
    dpg.set_value('program_status', 'Creating an XsControl object...\n')
    print('Creating an XsControl object... ')
    control = xda.XsControl()
    xda_version = xda.XsVersion()
    xda.xdaVersion(xda_version)
    if control != 0:
        dpg.set_value('program_status', f'XsControl object created successfully.\nXsens Device API version: {xda_version.toXsString()}\n{dpg.get_value("program_status")}')
        print(f'XsControl object created successfully.\nXsens Device API version: {xda_version.toXsString()}\n')
    # create XdaDongle object and set it up for recording
    try:
        dngl = xd.XdaDongle(control) # XsControl object as an argument for the __init__ method
        dngl.setDongle()
        dngl.setRadio()
        dngl.setMTw2s()
        dngl.setMTw2Locations()
        dngl.setRecording(log_path) # log file path as an argument for the setRecording method
    except Exception as e:
        dpg.set_value('program_status', f'{e}. Aborting.\n\n{dpg.get_value("program_status")}')
        print(f'{e} Aborting')
        sys.exit(1)
    # set MTw2 sensors' status and id
    try:
        # set MTw2 sensor status on the dashboard
        sf.status(dngl.mtw2s, dngl.mtw2_locations, ids=True)
        # set MTw2 sensor ids to dashboard plots and normalisation dictionary
        sf.set_sensor_ids(dngl.mtw2_ids, dngl.mtw2_locations)
    except Exception as e:
        dpg.set_value('program_status', f'{e}. Aborting.\n\n{dpg.get_value("program_status")}')
        print(f'{e} Aborting')
        sys.exit(1)    
    # create Open Sound Control server and client for sending sensor data to OSC environment
    try:          
        # set logger
        logging.basicConfig(format='%(asctime)s - %(processName)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARNING)
        logger = logging.getLogger('logger')            
        # install the osc4py3 tools with logger
        osc_startup(logger=logger)
        # set osc4py3 server for testing the OSC messages sent by OSC client: ip, port, name
        osc_udp_server(osc_server_ip, osc_server_port, 'OSC_server')
        # set handler function for osc4py3 messages
        osc_method('/test/*', sf.handler)
        # set osc4py3 client: ip, port, name
        osc_udp_client(osc_client_ip, osc_client_port, 'OSC_client')
    except Exception as e:
        dpg.set_value('program_status', f'{e}. Aborting.\n\n{dpg.get_value("program_status")}')
        print(f'{e} Aborting')
        sys.exit(1)        
    # start recording
    try:
        dngl.dongle.startRecording() 
        dpg.set_value('program_status', f'AW-DNG {dngl.dongle.deviceId()} is recording the connected MTw2 sensors\n{dpg.get_value("program_status")}')
        print(f'AW-DNG {dngl.dongle.deviceId()} is recording the connected MTw2 sensors')
    except: 
        dpg.set_value('program_status', f'AW-DNG {dngl.dongle.deviceId()} failed to start recording. Aborting.\n\n{dpg.get_value("program_status")}')
        print(f'AW-DNG {dngl.dongle.deviceId()} failed to start recording. Aborting.')
        sys.exit(1)
    dpg.set_value('program_status', f'Use dashboard "stop recording" button to stop\n\n{dpg.get_value("program_status")}')
    print('Use dashboard "stop recording" button to stop\n') 
    # variables for total acceleration binary trigger
    count_from = 0  # set timeout counter
    timeout = 0.2 # timeout (s) during which the program does not register a new hit from acceleration 
    # recording loop
    while not stop_rec: 
        # message variable for sending MTw2 sensor data to Open Sound Control environment
        osc_msg = []
        # check if a data packet is available
        if dngl.callback.packetAvailable():
            # get the data packet
            packet = dngl.callback.getNextPacket()
            # check if MTw2 id from which the packet is is available
            if packet.containsStoredDeviceId():
                # append MTw2 id for Open Sound Control message
                mtw2_id = f'{packet.deviceId()}'  
                # # xy where x is dancer number and y is 1 for left, 2 for right and 3 for middle
                osc_msg.append(dngl.mtw2_locations[mtw2_id][1])                       
            # check for calibrated data
            if packet.containsCalibratedData():
                # get acceleration data 
                acc = packet.calibratedAcceleration()
                acc_value = sf.normalise(mtw2_id, 'acc', [acc[0], acc[1], acc[2]])
                # get total acceleration as Euclidean norm of acceleration
                #tot_a_value = sf.normalise(mtw2_id, 'tot_a', [sqrt(acc[0]**2 + acc[1]**2 + acc[2]**2)]) 
                # set total acceleration to 1 or 0 with chosen threshold and timeout
                if sqrt(acc[0]**2 + acc[1]**2 + acc[2]**2) > acc_threshold and time.time() - count_from > timeout:
                    # first value is the measured total acceleration
                    tot_a_value = [sqrt(acc[0]**2 + acc[1]**2 + acc[2]**2), 1]
                    # set new time to count timeout from
                    count_from= time.time()
                elif sqrt(acc[0]**2 + acc[1]**2 + acc[2]**2) <= acc_threshold:
                    # first value is the measured total acceleration
                    tot_a_value = [sqrt(acc[0]**2 + acc[1]**2 + acc[2]**2), 0]
                # append acceleration data to Open Sound Control message
                acc_value = [round(val, 5) for val in acc_value]
                osc_msg.append(acc_value)
                osc_msg.append(round(tot_a_value[0], 5))
                # send acceleration data to dashboard plot
                sf.send_data(mtw2_id, dngl.mtw2_ids, 'acc', acc_value) 
                sf.send_data(mtw2_id, dngl.mtw2_ids, 'tot_a', tot_a_value) 
                # get gyroscope data
                gyr = packet.calibratedGyroscopeData() 
                gyr_value = sf.normalise(mtw2_id, 'gyr', [gyr[0], gyr[1], gyr[2]])                   
                # get rate of turn from gyroscope data
                rot_value = sf.normalise(mtw2_id, 'rot', [sqrt(gyr[0]**2 + gyr[1]**2 + gyr[2]**2)])                  
                # append gyroscope and rate of turn data to Open Sound Control message
                gyr_value = [round(val, 5) for val in gyr_value]
                osc_msg.append(gyr_value)
                osc_msg.append(round(rot_value[0], 5))
                # send gyroscope and rate of turn data to dashboard plot
                sf.send_data(mtw2_id, dngl.mtw2_ids, 'gyr', gyr_value)
                sf.send_data(mtw2_id, dngl.mtw2_ids, 'rot', rot_value)                        
                # get magnetic field data 
                mag = packet.calibratedMagneticField()
                mag_value = [round(val, 5) for val in sf.normalise(mtw2_id, 'mag', [mag[0], mag[1], mag[2]])]                   
                # append magnetic field data to Open Sound Control message
                osc_msg.append(mag_value)
                # send magnetic field data to dashboard plot
                sf.send_data(mtw2_id, dngl.mtw2_ids, 'mag', mag_value)                       
            # check for orientation data 
            if packet.containsOrientation():
                # get orientation data as Euler angles
                euler = packet.orientationEuler() 
                euler_value = [round(val, 5) for val in sf.normalise(mtw2_id, 'ori', [euler.x(), euler.y(), euler.z()])]                   
                # append Euler angles data to Open Sound Control message
                osc_msg.append(euler_value)                 
                # send Euler angles data to dashboard plot
                sf.send_data(mtw2_id, dngl.mtw2_ids, 'ori', euler_value)                             
            # send data from the data packet to Open Sound Control environment
            message = oscbuildparse.OSCMessage('/test/*', None, osc_msg)
            osc_send(message, 'OSC_client')
            osc_process()              
        # get measurement status of MTw2 sensors
        sf.status(dngl.mtw2s, dngl.mtw2_locations)                
    # uninstall the osc4py3 tools
    osc_terminate()
    # set measurement status of MTw2 sensors to 'Finished'
    sf.status(dngl.mtw2s, dngl.mtw2_locations, finished=True) 
    # stop recording and close all devices
    dpg.set_value('program_status', f'Closing AW-DNG2 {dngl.dongle.deviceId()}...\n{dpg.get_value("program_status")}')
    print(f'Closing AW-DNG2 {dngl.dongle.deviceId()}...')    
    try: 
        # stop recording
        dngl.dongle.stopRecording()
        dpg.set_value('program_status', f'AW-DNG2 {dngl.dongle.deviceId()} recording stopped...\n{dpg.get_value("program_status")}')
        print(f'AW-DNG2 {dngl.dongle.deviceId()} recording stopped', end='')
    except:
        dpg.set_value('program_status', f'Failed to stop AW-DNG2 {dngl.dongle.deviceId()} recording. Aborting.\n\n{dpg.get_value("program_status")}')
        print(f'\nFailed to stop AW-DNG2 {dngl.dongle.deviceId()} recording. Aborting.')
        sys.exit(1)
    # close log file
    if not dngl.dongle.closeLogFile():
        dpg.set_value('program_status', f'Failed to close AW-DNG2 {dngl.dongle.deviceId()} log file. Aborting.\n\n{dpg.get_value("program_status")}') 
        print(f'\nFailed to close AW-DNG2 {dngl.dongle.deviceId()} log file. Aborting.')  
        sys.exit(1)
    dpg.set_value('program_status', f'... and log file closed.\n{dpg.get_value("program_status")}')
    print(' and log file closed.')
    # remove callback handlers
    try:
        dngl.dongle.clearCallbackHandlers()
        dpg.set_value('program_status', f'AW-DNG2 {dngl.dongle.deviceId()} callback handler removed\n{dpg.get_value("program_status")}')
        print(f'AW-DNG2 {dngl.dongle.deviceId()} callback handler removed')
    except:
        dpg.set_value('program_status', f'Failed to remove callback handler from AW-DNG2 {dngl.dongle.deviceId()}. Aborting\n\n{dpg.get_value("program_status")}')
        print(f'Failed to remove callback handler from AW-DNG2 {dngl.dongle.deviceId()}. Aborting.')
        sys.exit(1)
    # close radio, port and control object
    try:
        # disable radio
        dngl.dongle.disableRadio()
        dpg.set_value('program_status', f'AW-DNG2 {dngl.dongle.deviceId()} radio disabled\n{dpg.get_value("program_status")}')
        print(f'AW-DNG2 {dngl.dongle.deviceId()} radio disabled')
        dpg.set_value('program_status', f'All devices closed. Closing the ports...\n\n{dpg.get_value("program_status")}')
        print('\nAll devices closed. Closing the ports...')
        # close the port
        for port in dngl.port:
            dngl.control.closePort(port.portName())
            dpg.set_value('program_status', f'Port {port.portName()} closed\n{dpg.get_value("program_status")}')
            print(f'Port {port.portName()} closed')
        # close control object
        dpg.set_value('program_status', f'All ports closed. Closing the XsControl object...\n{dpg.get_value("program_status")}')
        print('All ports closed. Closing the XsControl object...')
        dngl.control.close()
        dpg.set_value('program_status', f'XsControl object closed\n{dpg.get_value("program_status")}')
        print('XsControl object closed')
    except Exception as error:
        dpg.set_value('program_status', f'{error}. Aborting \n\n{dpg.get_value("program_status")}')
        print(f'{error}. Aborting')
        sys.exit(1)
    # succesful exit
    dpg.set_value('program_status', f'Successful exit. Ready for restart\n\n{dpg.get_value("program_status")}')
    print('Successful exit. Ready for restart')
