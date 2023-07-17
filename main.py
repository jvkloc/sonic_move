# Sonic Move Biodata Sonata main script.
import sys
import logging
import argparse
from pathlib import Path

# https://dearpygui.readthedocs.io/en/latest/
import dearpygui.dearpygui as dpg
# https://osc4py3.readthedocs.io/en/latest/
from osc4py3.as_eventloop import * 
from osc4py3 import oscbuildparse

import dashboard as db


def osc(server_ip, server_port, client_ip, client_port):
   """osc function sets up Open Sound Control messaging between a server
   and a client.
   Parameters
   --------------
   server_ip :
       IP address of Open Sound Control server.
   server_port :
       Open Sound Control port.
   client_ip :
       IP address of Open Sound Control client.
   client_port :
       Open Sound Control client port.
   """
   logging.basicConfig(
       format='%(asctime)s - %(processName)s - %(name)s'
        ' - %(levelname)s - %(message)s', level=logging.WARNING
    )
   logger = logging.getLogger('logger')
   osc_startup(logger=logger)
   osc_udp_server(server_ip, server_port, 'OSC_server')
   osc_udp_client(client_ip, client_port, 'OSC_client')
   

def osc_handler(acc, tot_acc, gyr, rot, mag, ori, mtw2_id):
   print(acc, tot_acc, gyr, rot, mag, ori, mtw2_id)

                                                    
def main():
   """Sonic Move Biodata sonata main script. 
   Arguments
   ---------
   server_ip : str
       IP address of Open Sound Control server.
   server_port : int
       Open Sound Control port.
   client_ip : str
       IP address of Open Sound Control client.
   client_port : int
       Open Sound Control client port.
   device : str
       'dongle' or 'station' Xsens main device. Default is 'station'.
   path : str
       File path for saving log files. Recommendation is to create a 
       folder just for the logs. 
   """
   parser = argparse.ArgumentParser()
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
   parser.add_argument(
       '--device', '-d', type=str, default='station',
        help='Xsens main device: "dongle" or "station".'
    )
   parser.add_argument(
       '--path', '-p', type=str, default=r'C:\Users\wksadmin\Downloads\lokit',
        help='File path for saving log files.'
    )    
   args = parser.parse_args()
   
   try:          
      osc(args.server_ip, args.server_port, args.client_ip, args.client_port)
   except Exception as e:
      print(f'{e}. Open Sound Control setup failed. Aborting')
      sys.exit(1)
   try:
      dashboard = db.Dashboard(args.device, Path(args.path))   
   except Exception as e:
      print(f'{e}. Dashboard setup failed. Aborting.')
      sys.exit(1)
   dpg.setup_dearpygui()
   dpg.maximize_viewport()
   dpg.show_viewport()
   dpg.start_dearpygui()
   dpg.destroy_context()

if __name__ == '__main__':
   main()
