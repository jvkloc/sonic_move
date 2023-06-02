# Xsens Device API documentation provided with SDK download from https://www.movella.com/support/software-documentation
import xsensdeviceapi as xda
import XdaCallback as xc
import dearpygui.dearpygui as dpg # https://dearpygui.readthedocs.io/en/latest/
from math import floor
import time
import sys
# class for Awinda Dongle and attached MTw2 sensors
class XdaDongle():
    # XsControl object as an argument for the __init__ method
    def __init__(self, control):
        self.control = control 
        self.port = None
        self.dongle = None 
        self.callback = None
        self.chnls = ' '.join(map(str, list(range(11,26)))) # available channels from Movella documentation
        self.slctd_chnl= 11 # hardcoded for Minimi's Biodata Sonate
        self.reserved_chnls = [11] # hardcoded for Minimi's Biodata Sonate
        self.update_rates = None
        self.slctd_update_rate = 100 # hardcoded for Minimi's Biotada Sonate          
        self.mtw2s = []
        self.mtw2_ids = [] 
        self.mtw2_locations = {}
    
    def setDongle(self):       
        # scan ports for Xsens device
        dpg.set_value('program_status', f'Scanning for ports with Xsens devices...\n{dpg.get_value("program_status")}')
        print('Scanning for ports with Xsens devices...')
        self.port = xda.XsScanner_scanPorts()
        # print Xsens device port info or exit if no Xsens device is found
        if len(self.port) > 0:
            for port in self.port:
                dpg.set_value('program_status', f'The following port with a connected Xsens device was found:\n{dpg.get_value("program_status")}')
                print('The following port with a connected Xsens device was found:')
                dpg.set_value('program_status', f'{port.portName()} with baud rate {port.baudrate()} Bd and device id {port.deviceId()}\n{dpg.get_value("program_status")}')
                print(f'{port.portName()} with baud rate {port.baudrate()} Bd and device id {port.deviceId()}')
        else:
            dpg.set_value('program_status', f'No Xsens device found. Aborting\n\n{dpg.get_value("program_status")}')
            print('No Xsens device found. Aborting')
            sys.exit(1)
        # get the Awinda Dongle connected to the port or exit if the Xsens device is of another type
        dpg.set_value('program_status', f'Checking the type of the connected Xsens device...\n\n{dpg.get_value("program_status")}')
        print('\nChecking the type of the connected Xsens device...')
        for port in self.port:
            if port.deviceId().isAwinda2Dongle():
                dpg.set_value('program_status', f'Device {port.deviceId()} is of type AW-DNG2\n{dpg.get_value("program_status")}')
                print(f'Device {port.deviceId()} is of type AW-DNG2')
            else:
                dpg.set_value('program_status', f'AW-DNG2 device not found. Aborting.\n\n{dpg.get_value("program_status")}')
                print('AW-DNG2 device not found. Aborting.')
                sys.exit(1)
        # open the Awinda Dongle port
        dpg.set_value('program_status', f'Opening Dongle port...\n\n{dpg.get_value("program_status")}')
        print('\nOpening Dongle port...')
        for port in self.port:
            if not self.control.openPort(port.portName(), port.baudrate()):
                dpg.set_value('program_status', f'Unable to open Dongle port. Aborting.\n\n{dpg.get_value("program_status")}')
                print('Unable to open Dongle port. Aborting.')
                sys.exit(1)
            # use the Awinda Dongle id to initialise it as a contol object device and notify the user
            self.dongle = self.control.device(port.deviceId())
            dpg.set_value('program_status', f'Port {port.portName()} for AW-DNG2 {port.deviceId().toXsString()} opened\n{dpg.get_value("program_status")}')
            print(f'Port {port.portName()} for AW-DNG2 {port.deviceId().toXsString()} opened') 
        # set callback handler and live data recording options for the Awinda Dongle
        try:
            # set callback handler for the Awinda Dongle
            callback = xc.XdaCallback()
            self.dongle.addCallbackHandler(callback)
            # save callback handler to the XdaDongle object for MTw2 sensor configuration
            self.callback = callback
            # set Awinda Dongle live data recording options
            self.dongle.setOptions(xda.XSO_RetainLiveData or xda.XSO_Orientation or XSO_OrientationInLiveStream, xda.XSO_None)
        except Exception as e:
            dpg.set_value('program_status', f'{e}. Aborting \n\n{dpg.get_value("program_status")}')
            print(f'{e}. Aborting')
            sys.exit(1)
            
    def setRadio(self):
        # go to config for setting radio channel and baudrate
        self.dongle.gotoConfig()  
        try:
            self.update_rates = self.dongle.supportedUpdateRates(xda.XSO_None)
        except:
            dpg.set_value('program_status', f'Failed to get supported update rates for AW-DNG2 {self.dongle.deviceId()}. Aborting.\n\n{dpg.get_value("program_status")}')
            print(f'Failed to get supported update rates for AW-DNG2 {self.dongle.deviceId()}. Aborting.')
            sys.exit(1)
        self.dongle.enableRadio(self.slctd_chnl)
        # choose and set update rates and choose radio channels, hardcoded for Minimi's Biodata Sonate        
        #print(f'Available radio channels are {self.chnls}')
        #print('Recommended wireless update rates are:')
        #print('  60Hz for 11 - 20 MTw sensors\n  80Hz for     10    MTw sensors\n100Hz for   6 - 9   MTw sensors\n120Hz for   1 - 5   MTw sensors')
        #rates = f'{"Hz ".join(map(str, self.update_rates))} Hz'    
        #print(f'\nSupported update rates for AW-DNG2 {self.dongle.deviceId()}: {rates}')
        #slctd_update_rate = int(input(f'Select one of the supported update rates for AW-DNG2 {self.dongle.deviceId()}: '))
        #slctd_chnl = int(input(f'Select one of the available radio channels for AW-DNG2 {self.dongle.deviceId()}: ')) 
        #if slctd_rate in update_rates:
        #    self.dongle.setUpdateRate(self.slctd_update_rate)
        #else:
        #    dpg.set_value('program_status', f'The selected update rate is not supported.Aborting\n\n{dpg.get_value("program_status")}')
        #   print('The selected update rate is not supported. Aborting.')
        #    sys.exit(1)
        # enable radios
        #if self.slctd_chnl not in reserved_chnls:
        #    self.dongle.enableRadio(self.slctd_chnl)
        #    reserved_chnls.append(self.slctd_chnl)
        dpg.set_value('program_status', f'AW-DNG2 {self.dongle.deviceId()} update rate set to {self.slctd_update_rate} Hz and radio enabled on channel {self.slctd_chnl}\n{dpg.get_value("program_status")}')
        print(f'AW-DNG2 {self.dongle.deviceId()} update rate set to {self.slctd_update_rate} Hz and radio enabled on channel {self.slctd_chnl}')
    
    def setMTw2s(self):
        # assuming Dongle is already in config mode after setRadio(): wait for the MTw2 sensors to connect
        dpg.set_value('program_status', f'Connecting the MTw2 sensors to AW-DNG2 {self.dongle.deviceId()}...\n\n{dpg.get_value("program_status")}')
        print(f'\nConnecting the MTw2 sensors to AW-DNG2 {self.dongle.deviceId()}...')
        time.sleep(5)
        # confirm that the MTw2 sensors are connected
        dpg.set_value('program_status', f'{self.dongle.childCount()} MTw2 sensors connected to AW-DNG2 {self.dongle.deviceId()} initialised\n{dpg.get_value("program_status")}')
        print(f'{self.dongle.childCount()} MTw2 sensors connected to AW-DNG2 {self.dongle.deviceId()} initialised')
        dpg.set_value('program_status', f'Configuring the connected MTw2 sensors...\n{dpg.get_value("program_status")}')
        print('Configuring the connected MTw2 sensors...')
        # setup for attached MTw2 sensors
        for mtw in self.dongle.children():
           # save MTw2 sensors and ids
            self.mtw2_ids.append(f'{mtw.deviceId()}')
            self.mtw2s.append(mtw)
            # add configuration for data types
            mtw.gotoConfig()
            config_array = xda.XsOutputConfigurationArray()
            config_array.push_back(xda.XsOutputConfiguration(xda.XDI_PacketCounter, 0))
            config_array.push_back(xda.XsOutputConfiguration(xda.XDI_SampleTimeFine, 0)) 
            config_array.push_back(xda.XsOutputConfiguration(xda.XDI_Acceleration, 0xFFFF))
            config_array.push_back(xda.XsOutputConfiguration(xda.XDI_EulerAngles, 0xFFFF))
            # set the array to the MTw2
            if not mtw.setOutputConfiguration(config_array):
                dpg.set_value('program_status', f'Configuration of MTw2 sensor {mtw.deviceId()} failed. Aborting.\n\n{dpg.get_value("program_status")}')
                raise RuntimeError(f'Configuration of MTw2 sensor {mtw.deviceId()} failed. Aborting.')
    
    def setMTw2Locations(self):
        # locations for dancer number and body position of MTw2 sensors
        locations = ['left', 'right', 'middle']
        # place MTw2 sensors in order dancer one, left, right, middle and similarly for dancers two and three
        for i in range(len(self.mtw2_ids)): 
            # second value is id for Open Sound Control Message
            self.mtw2_locations[self.mtw2_ids[i]] = [f'Dancer {floor(i/3)+1} {locations[i-floor(i/3)*3]}', f'{floor(i/3)+1}{i+1-floor(i/3)*3}']           
    
    def setRecording(self, log_path):
        # set the Dongle and connected sensors to measurement mode
        try:
            self.dongle.gotoMeasurement()
        except Exception as e:
            dpg.set_value('program_status', f'Failed to set AW-DNG2 {self.dongle.deviceId()} to measurement mode. Aborting.\n\n{dpg.get_value("program_status")}')
            print(f'Failed to set AW-DNG2 {self.dongle.deviceId()} to measurement mode. Aborting.')  
            sys.exit(1)
        # check that the MTw2s are in measurement mode
        for mtw in self.mtw2s:
            if mtw.isMeasuring():
                dpg.set_value('program_status', f'MTw2 {mtw.deviceId()} connected to AW-DNG2 {self.dongle.deviceId()} set to measurement mode\n{dpg.get_value("program_status")}')
                print(f'MTw2 {mtw.deviceId()} connected to AW-DNG2 {self.dongle.deviceId()} set to measurement mode')
        # create log file
        dpg.set_value('program_status', f'Creating a log file for AW-DNG2 {self.dongle.deviceId()} and starting recording...\n\n{dpg.get_value("program_status")}')
        print(f'\nCreating a log file for AW-DNG2 {self.dongle.deviceId()} and starting recording...')
        log = f'{log_path}{self.dongle.deviceId()}_log.mtb'
        if self.dongle.createLogFile(log) != xda.XRV_OK:
            dpg.set_value('program_status', f'Failed to create a log file for AW-DNG2 {self.dongle.deviceId()}. Aborting.\n\n{dpg.get_value("program_status")}')
            print(f'Failed to create a log file for AW-DNG2 {self.dongle.deviceId()}. Aborting.')
            sys.exit(1)
