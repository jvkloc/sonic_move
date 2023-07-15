# https://osc4py3.readthedocs.io/en/latest/
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse


def osc(server_ip, server_port, client_ip, client_port):
    """osc sets up Open Sound Control messaging between a
    server and a client.
    """
    logging.basicConfig(
        format='%(asctime)s - %(processName)s - %(name)s'
        ' - %(levelname)s - %(message)s', level=logging.WARNING
    )
    logger = logging.getLogger('logger')
    osc_startup(logger=logger)
    osc_udp_server(server_ip, server_port, 'OSC_server')
    osc_udp_client(client_ip, client_port, 'OSC_client')
